import React, { useState, useEffect } from "react";
import axios from "axios";

const API = "http://localhost:5000/api";

function ActivityLog() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = async () => {
    try {
      const res = await axios.get(`${API}/admin/activity`);
      setLogs(res.data.logs);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  const getActionStyle = (action) => {
    if (action.includes("approved") || action.includes("publish")) return "bg-emerald-100 text-emerald-700";
    if (action.includes("flagged")) return "bg-amber-100 text-amber-700";
    if (action.includes("reject")) return "bg-red-100 text-red-700";
    return "bg-gray-100 text-gray-700";
  };

  if (loading) {
    return <div className="text-center py-20 text-gray-500">Loading...</div>;
  }

  if (logs.length === 0) {
    return (
      <div className="bg-white border border-gray-200 rounded-xl p-12 text-center shadow-sm">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">No Activity Yet</h3>
        <p className="text-gray-500 text-sm">AI agent activity will appear here.</p>
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">
          Activity Log ({logs.length} entries)
        </h2>
        <button
          onClick={fetchLogs}
          className="text-sm text-indigo-600 hover:text-indigo-700 font-medium"
        >
          Refresh
        </button>
      </div>

      <div className="bg-white border border-gray-200 rounded-xl divide-y divide-gray-100 shadow-sm">
        {logs.map((log) => (
          <div key={log.id} className="p-4 flex items-start gap-4">
            <span className={`text-xs font-medium px-2 py-1 rounded-full mt-1 whitespace-nowrap ${getActionStyle(log.action)}`}>
              {log.action.replace(/_/g, " ")}
            </span>
            <div className="flex-1 min-w-0">
              <p className="text-sm text-gray-900 font-medium">{log.details}</p>
              <div className="flex gap-4 mt-1 text-xs text-gray-400">
                <span>{log.actor}</span>
                <span>{log.timestamp}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ActivityLog;