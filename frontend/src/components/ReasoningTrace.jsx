import React, { useState } from "react";

const KIND_STYLE = {
  thought: { label: "Thought", pill: "bg-indigo-100 text-indigo-700", dot: "bg-indigo-400" },
  tool_call: { label: "Tool Call", pill: "bg-blue-100 text-blue-700", dot: "bg-blue-400" },
  tool_result: { label: "Tool Result", pill: "bg-sky-100 text-sky-700", dot: "bg-sky-400" },
  decision: { label: "Decision", pill: "bg-emerald-100 text-emerald-700", dot: "bg-emerald-500" },
};

function ReasoningTrace({ trace }) {
  const [open, setOpen] = useState(false);

  if (!trace || trace.length === 0) {
    return (
      <p className="text-xs text-gray-400 italic">
        No reasoning trace recorded for this item.
      </p>
    );
  }

  const toolSteps = trace.filter((s) => s.kind === "tool_call").length;

  return (
    <div className="border border-gray-200 rounded-lg">
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-full flex items-center justify-between px-4 py-2 text-left hover:bg-gray-50 transition-colors"
      >
        <span className="text-sm font-semibold text-gray-700">
          AI Reasoning Trace
          <span className="ml-2 text-xs font-normal text-gray-400">
            {trace.length} steps, {toolSteps} tool call{toolSteps === 1 ? "" : "s"}
          </span>
        </span>
        <span className="text-gray-400 text-xs">{open ? "Hide" : "Show"}</span>
      </button>

      {open && (
        <ol className="divide-y divide-gray-100 border-t border-gray-100">
          {trace.map((step, i) => {
            const style = KIND_STYLE[step.kind] || {
              label: step.kind,
              pill: "bg-gray-100 text-gray-700",
              dot: "bg-gray-400",
            };
            return (
              <li key={i} className="px-4 py-3">
                <div className="flex items-center gap-2 mb-1">
                  <span className={`w-2 h-2 rounded-full ${style.dot}`}></span>
                  <span className="text-[11px] text-gray-400">
                    Step {step.step_number}
                  </span>
                  <span className={`text-[11px] font-medium px-2 py-0.5 rounded-full ${style.pill}`}>
                    {style.label}
                  </span>
                  {step.tool_name && (
                    <span className="text-[11px] font-mono text-gray-500">
                      {step.tool_name}
                    </span>
                  )}
                </div>

                <p className="text-sm text-gray-700 whitespace-pre-wrap ml-4">
                  {step.content}
                </p>

                {step.tool_input && Object.keys(step.tool_input).length > 0 && (
                  <pre className="ml-4 mt-2 text-[11px] bg-gray-50 border border-gray-100 rounded p-2 overflow-x-auto text-gray-600">
                    input: {JSON.stringify(step.tool_input)}
                  </pre>
                )}

                {step.tool_output && (
                  <pre className="ml-4 mt-1 text-[11px] bg-gray-50 border border-gray-100 rounded p-2 overflow-x-auto text-gray-600 max-h-48">
                    {JSON.stringify(step.tool_output, null, 2)}
                  </pre>
                )}
              </li>
            );
          })}
        </ol>
      )}
    </div>
  );
}

export default ReasoningTrace;
