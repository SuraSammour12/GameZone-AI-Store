import React, { useState, useEffect } from "react";
import axios from "axios";
import ReasoningTrace from "./ReasoningTrace";

const API = "http://localhost:5000/api";

function FlaggedOrders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      const res = await axios.get(`${API}/orders?status=flagged`);
      setOrders(res.data.orders);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  const handleDecision = async (orderId, action) => {
    try {
      await axios.post(`${API}/orders/${orderId}/decide`, {
        action,
        note: action === "reject" ? "Rejected by admin" : "Approved after review",
      });
      fetchOrders();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return <div className="text-center py-20 text-gray-500">Loading...</div>;
  }

  if (orders.length === 0) {
    return (
      <div className="bg-white border border-gray-200 rounded-xl p-12 text-center shadow-sm">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">No Flagged Orders</h3>
        <p className="text-gray-500 text-sm">All orders are clear. The AI is watching.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold text-gray-900">
        Flagged Orders ({orders.length})
      </h2>

      {orders.map((order) => (
        <div
          key={order.id}
          className="bg-white border border-amber-200 rounded-xl p-5 shadow-sm"
        >
          <div className="flex items-center justify-between mb-4">
            <div>
              <span className="font-semibold text-gray-900">{order.id}</span>
              <span className="text-sm text-gray-500 ml-3">{order.customer_name}</span>
            </div>
            <span className="text-xs bg-amber-100 text-amber-700 px-3 py-1 rounded-full font-medium">
              {order.ai_analysis && order.ai_analysis.risk_level
                ? order.ai_analysis.risk_level.toUpperCase() + " RISK"
                : "FLAGGED"}
            </span>
          </div>

          {/* Items */}
          <div className="bg-gray-50 rounded-lg p-3 mb-4">
            {order.items.map((item, i) => (
              <div key={i} className="flex justify-between text-sm py-1">
                <span className="text-gray-600">
                  {item.product_name} x{item.quantity}
                  <span className={`ml-2 text-xs ${
                    item.age_rating.includes("18") || item.age_rating.includes("17")
                      ? "text-red-500" : "text-emerald-500"
                  }`}>
                    ({item.age_rating})
                  </span>
                </span>
                <span className="font-medium text-gray-900">${item.subtotal}</span>
              </div>
            ))}
            <div className="border-t border-gray-200 mt-2 pt-2 flex justify-between font-semibold">
              <span>Total</span>
              <span>${order.total}</span>
            </div>
          </div>

          {/* AI Analysis */}
          {order.ai_analysis && (
            <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-4">
              <p className="text-sm font-semibold text-amber-700 mb-1">AI Analysis:</p>
              <p className="text-sm text-amber-600 mb-2">{order.ai_analysis.reason}</p>
              {order.ai_analysis.flags && order.ai_analysis.flags.length > 0 && (
                <div className="flex gap-2 flex-wrap mb-2">
                  {order.ai_analysis.flags.map((flag, i) => (
                    <span key={i} className="text-xs bg-amber-100 text-amber-700 px-2 py-1 rounded-full">
                      {flag}
                    </span>
                  ))}
                </div>
              )}
              {order.ai_analysis.recommendation && (
                <p className="text-xs text-gray-600">
                  Recommendation: {order.ai_analysis.recommendation}
                </p>
              )}
            </div>
          )}

          {/* Reasoning Trace */}
          {order.ai_analysis && (
            <div className="mb-4">
              <ReasoningTrace trace={order.ai_analysis.reasoning_trace} />
            </div>
          )}

          <div className="flex gap-3 justify-end">
            <button
              onClick={() => handleDecision(order.id, "reject")}
              className="px-5 py-2 rounded-lg text-sm font-medium bg-white text-red-600 border border-red-300 hover:bg-red-50 transition-colors"
            >
              Reject
            </button>
            <button
              onClick={() => handleDecision(order.id, "approve")}
              className="px-5 py-2 rounded-lg text-sm font-medium bg-emerald-600 text-white hover:bg-emerald-700 transition-colors"
            >
              Approve
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default FlaggedOrders;
