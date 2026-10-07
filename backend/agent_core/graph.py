import json

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.graph import END, START, StateGraph

from .config import build_llm
from .rules import (
    compute_order_flags,
    load_policy,
    load_recent_overrides,
    review_first_pass,
    reviewer_status,
)
from .schemas import OrderDecision, ReviewDecision
from .state import (
    MAX_ITERATIONS,
    OrderAgentState,
    ReviewAgentState,
    new_reasoning_step,
)
from .tools.order_tools import ORDER_TOOLS
from .tools.review_tools import REVIEW_TOOLS


ORDER_SYSTEM_PROMPT = (
    "You are the fraud triage agent for GameZone, an online gaming store. "
    "Your job is to decide whether an order should be approved or flagged for a "
    "human admin to review.\n\n"
    "The policy checks that rely on exact numbers have already been computed for "
    "you and are provided as hard flags. Do not recompute totals, item counts, or "
    "thresholds yourself. Your task is judgment: use the tools to investigate the "
    "customer's history, the delivery address, and any reselling or past-rejection "
    "patterns, then weigh the hard flags against that history.\n\n"
    "A hard flag is a reason to look closer, not an automatic rejection. A trusted "
    "customer with a long clean history who trips a single threshold may still be a "
    "legitimate buyer. A new customer with no history whose order matches a known "
    "fraud pattern should be flagged. Call tools until you have enough evidence, "
    "then stop calling tools and state your conclusion in plain language."
)

ORDER_DECISION_PROMPT = (
    "Produce the final decision now as structured output. Base it on the hard flags "
    "and everything the tools returned. If you are flagging, make the flags specific "
    "and the recommendation actionable for the admin."
)

REVIEW_SYSTEM_PROMPT = (
    "You are the content moderation agent for GameZone, an online gaming store. "
    "Your job is to decide whether a customer review should be auto-published or "
    "flagged for a human admin.\n\n"
    "Cheap deterministic checks have already run and are provided as hard flags "
    "(links, exact-duplicate text). Your task is judgment: use the tools to check "
    "the reviewer's history, compare the text against known spam, verify the buyer "
    "actually purchased the product, and confirm the review is about this product. "
    "Then decide.\n\n"
    "Negative reviews are allowed when they are respectful and about the product "
    "(criticism of graphics, price, or gameplay is fine). Flag offensive language, "
    "insults, threats, spam, promotion, off-topic content, or reviews from accounts "
    "with no matching purchase and only generic praise. Call tools until you have "
    "enough evidence, then stop and state your conclusion in plain language."
)

REVIEW_DECISION_PROMPT = (
    "Produce the final decision now as structured output. Base it on the hard flags "
    "and everything the tools returned."
)


def _tool_map(tools):
    return {t.name: t for t in tools}


ORDER_TOOL_MAP = _tool_map(ORDER_TOOLS)
REVIEW_TOOL_MAP = _tool_map(REVIEW_TOOLS)


def _order_prepare(state: OrderAgentState) -> dict:
    order = state["order"]
    policy = load_policy()
    hard_flags = compute_order_flags(order, policy)
    override_context = load_recent_overrides()

    summary = {
        "customer_name": order.get("customer_name"),
        "customer_address": order.get("customer_address"),
        "total": order.get("total"),
        "item_count": order.get("item_count"),
        "items": [
            {
                "product_id": i.get("product_id"),
                "product_name": i.get("product_name"),
                "price": i.get("price"),
                "quantity": i.get("quantity"),
                "age_rating": i.get("age_rating"),
            }
            for i in order.get("items", [])
        ],
    }

    human = (
        f"Order to review:\n{json.dumps(summary, indent=2)}\n\n"
        f"Hard flags computed by policy checks: "
        f"{hard_flags if hard_flags else 'none'}\n\n"
        f"{override_context}"
    )

    trace = [
        new_reasoning_step(
            1,
            "thought",
            f"Computed {len(hard_flags)} hard flag(s): {hard_flags or 'none'}.",
        )
    ]

    return {
        "hard_flags": hard_flags,
        "override_context": override_context,
        "messages": [SystemMessage(content=ORDER_SYSTEM_PROMPT), HumanMessage(content=human)],
        "reasoning_trace": trace,
        "iterations": 0,
    }


def _review_prepare(state: ReviewAgentState) -> dict:
    review = state["review"]
    hard_flags = review_first_pass(review)
    status = reviewer_status(review.get("customer_name", ""))

    summary = {
        "review_id": review.get("id"),
        "product_id": review.get("product_id"),
        "customer_name": review.get("customer_name"),
        "rating": review.get("rating"),
        "text": review.get("text"),
    }

    human = (
        f"Review to moderate:\n{json.dumps(summary, indent=2)}\n\n"
        f"Hard flags from first-pass checks: {hard_flags if hard_flags else 'none'}\n\n"
        f"{status}"
    )

    trace = [
        new_reasoning_step(
            1,
            "thought",
            f"First-pass flags: {hard_flags or 'none'}. {status}",
        )
    ]

    return {
        "hard_flags": hard_flags,
        "reviewer_status": status,
        "messages": [SystemMessage(content=REVIEW_SYSTEM_PROMPT), HumanMessage(content=human)],
        "reasoning_trace": trace,
        "iterations": 0,
    }


def _make_reason(llm_with_tools):
    def _reason(state) -> dict:
        trace = list(state["reasoning_trace"])
        response = llm_with_tools.invoke(state["messages"])

        step_no = len(trace) + 1
        if response.content:
            trace.append(new_reasoning_step(step_no, "thought", response.content))
            step_no += 1

        for call in response.tool_calls or []:
            trace.append(
                new_reasoning_step(
                    step_no,
                    "tool_call",
                    f"Calling {call['name']}",
                    tool_name=call["name"],
                    tool_input=call.get("args", {}),
                )
            )
            step_no += 1

        return {"messages": [response], "reasoning_trace": trace}

    return _reason


def _make_act(tool_map):
    def _act(state) -> dict:
        trace = list(state["reasoning_trace"])
        last = state["messages"][-1]
        tool_messages = []
        step_no = len(trace) + 1

        for call in last.tool_calls:
            tool = tool_map.get(call["name"])
            if tool is None:
                output = {"error": f"Unknown tool: {call['name']}"}
            else:
                try:
                    output = tool.invoke(call.get("args", {}))
                except Exception as exc:
                    output = {"error": f"{type(exc).__name__}: {exc}"}

            tool_messages.append(
                ToolMessage(content=json.dumps(output, default=str), tool_call_id=call["id"])
            )
            trace.append(
                new_reasoning_step(
                    step_no,
                    "tool_result",
                    f"Result from {call['name']}",
                    tool_name=call["name"],
                    tool_input=call.get("args", {}),
                    tool_output=output,
                )
            )
            step_no += 1

        return {
            "messages": tool_messages,
            "reasoning_trace": trace,
            "iterations": state["iterations"] + 1,
        }

    return _act


def _route(state) -> str:
    last = state["messages"][-1]
    if getattr(last, "tool_calls", None) and state["iterations"] < MAX_ITERATIONS:
        return "act"
    return "decide"


def _make_order_decide(llm):
    structured = llm.with_structured_output(OrderDecision)

    def _decide(state: OrderAgentState) -> dict:
        trace = list(state["reasoning_trace"])
        messages = state["messages"] + [HumanMessage(content=ORDER_DECISION_PROMPT)]
        result: OrderDecision = structured.invoke(messages)
        decision = result.model_dump()

        trace.append(
            new_reasoning_step(
                len(trace) + 1,
                "decision",
                f"{decision['decision']} (risk: {decision['risk_level']}) - {decision['reason']}",
            )
        )
        return {"final_decision": decision, "reasoning_trace": trace}

    return _decide


def _make_review_decide(llm):
    structured = llm.with_structured_output(ReviewDecision)

    def _decide(state: ReviewAgentState) -> dict:
        trace = list(state["reasoning_trace"])
        messages = state["messages"] + [HumanMessage(content=REVIEW_DECISION_PROMPT)]
        result: ReviewDecision = structured.invoke(messages)
        decision = result.model_dump()

        trace.append(
            new_reasoning_step(
                len(trace) + 1,
                "decision",
                f"{decision['decision']} ({decision['category']}) - {decision['reason']}",
            )
        )
        return {"final_decision": decision, "reasoning_trace": trace}

    return _decide


def build_order_graph():
    llm = build_llm()
    llm_with_tools = llm.bind_tools(ORDER_TOOLS)

    graph = StateGraph(OrderAgentState)
    graph.add_node("prepare", _order_prepare)
    graph.add_node("reason", _make_reason(llm_with_tools))
    graph.add_node("act", _make_act(ORDER_TOOL_MAP))
    graph.add_node("decide", _make_order_decide(llm))

    graph.add_edge(START, "prepare")
    graph.add_edge("prepare", "reason")
    graph.add_conditional_edges("reason", _route, {"act": "act", "decide": "decide"})
    graph.add_edge("act", "reason")
    graph.add_edge("decide", END)

    return graph.compile()


def build_review_graph():
    llm = build_llm()
    llm_with_tools = llm.bind_tools(REVIEW_TOOLS)

    graph = StateGraph(ReviewAgentState)
    graph.add_node("prepare", _review_prepare)
    graph.add_node("reason", _make_reason(llm_with_tools))
    graph.add_node("act", _make_act(REVIEW_TOOL_MAP))
    graph.add_node("decide", _make_review_decide(llm))

    graph.add_edge(START, "prepare")
    graph.add_edge("prepare", "reason")
    graph.add_conditional_edges("reason", _route, {"act": "act", "decide": "decide"})
    graph.add_edge("act", "reason")
    graph.add_edge("decide", END)

    return graph.compile()


_order_graph = None
_review_graph = None


def analyze_order(order: dict) -> dict:
    global _order_graph
    if _order_graph is None:
        _order_graph = build_order_graph()
    result = _order_graph.invoke(
        {"order": order, "messages": [], "reasoning_trace": [], "iterations": 0}
    )
    decision = result["final_decision"]
    decision["reasoning_trace"] = result["reasoning_trace"]
    return decision


def analyze_review(review: dict) -> dict:
    global _review_graph
    if _review_graph is None:
        _review_graph = build_review_graph()
    result = _review_graph.invoke(
        {"review": review, "messages": [], "reasoning_trace": [], "iterations": 0}
    )
    decision = result["final_decision"]
    decision["reasoning_trace"] = result["reasoning_trace"]
    return decision
