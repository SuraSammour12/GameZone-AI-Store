from typing import Annotated, Any, Optional
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


MAX_ITERATIONS = 8


class ReasoningStep(TypedDict):
    step_number: int
    kind: str
    content: str
    tool_name: Optional[str]
    tool_input: Optional[dict]
    tool_output: Optional[Any]


class OrderAgentState(TypedDict):
    order: dict
    hard_flags: list[str]
    override_context: str
    messages: Annotated[list[BaseMessage], add_messages]
    reasoning_trace: list[ReasoningStep]
    iterations: int
    final_decision: Optional[dict]


class ReviewAgentState(TypedDict):
    review: dict
    hard_flags: list[str]
    reviewer_status: str
    messages: Annotated[list[BaseMessage], add_messages]
    reasoning_trace: list[ReasoningStep]
    iterations: int
    final_decision: Optional[dict]


def new_reasoning_step(
    step_number: int,
    kind: str,
    content: str,
    tool_name: Optional[str] = None,
    tool_input: Optional[dict] = None,
    tool_output: Optional[Any] = None,
) -> ReasoningStep:
    return {
        "step_number": step_number,
        "kind": kind,
        "content": content,
        "tool_name": tool_name,
        "tool_input": tool_input,
        "tool_output": tool_output,
    }
