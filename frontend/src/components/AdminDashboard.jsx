import React, { useState, useEffect } from "react";
import axios from "axios";

const API = "http://localhost:5000/api";

function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await axios.get(`${API}/admin/stats`);
      setStats(res.data);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  const resetData = async () => {
    if (!window.confirm("Clear all data?")) return;
    await axios.post(`${API}/admin/reset`);
    fetchStats();
  };

  if (loading || !stats) {
    return <div className="text-center py-20 text-gray-500">Loading dashboard...</div>;
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-900">Admin Dashboard</h2>
        <button
          onClick={resetData}
          className="text-sm text-red-500 hover:text-red-700 font-medium"
        >
          Reset All Data
        </button>
      </div>

      {/* Order Stats */}
      <h3 className="text-sm font-semibold text-gray-500 mb-3 uppercase tracking-wide">Orders</h3>
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
        <div className="bg-white border border-gray-200 rounded-xl p-5 text-center shadow-sm">
          <p className="text-xs text-gray-500 mb-1">Total Orders</p>
          <p className="text-3xl font-bold text-gray-900">{stats.orders.total}</p>
        </div>
        <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-5 text-center">
          <p className="text-xs text-gray-500 mb-1">Approved</p>
          <p className="text-3xl font-bold text-emerald-600">{stats.orders.approved}</p>
        </div>
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-5 text-center">
          <p className="text-xs text-gray-500 mb-1">Flagged</p>
          <p className="text-3xl font-bold text-amber-600">{stats.orders.flagged}</p>
        </div>
        <div className="bg-red-50 border border-red-200 rounded-xl p-5 text-center">
          <p className="text-xs text-gray-500 mb-1">Rejected</p>
          <p className="text-3xl font-bold text-red-600">{stats.orders.rejected}</p>
        </div>
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-5 text-center">
          <p className="text-xs text-gray-500 mb-1">Revenue</p>
          <p className="text-2xl font-bold text-blue-600">${stats.orders.revenue}</p>
        </div>
      </div>

      {/* Review Stats */}
      <h3 className="text-sm font-semibold text-gray-500 mb-3 uppercase tracking-wide">Reviews</h3>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white border border-gray-200 rounded-xl p-5 text-center shadow-sm">
          <p className="text-xs text-gray-500 mb-1">Total Reviews</p>
          <p className="text-3xl font-bold text-gray-900">{stats.reviews.total}</p>
        </div>
        <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-5 text-center">
          <p className="text-xs text-gray-500 mb-1">Published</p>
          <p className="text-3xl font-bold text-emerald-600">{stats.reviews.published}</p>
        </div>
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-5 text-center">
          <p className="text-xs text-gray-500 mb-1">Flagged</p>
          <p className="text-3xl font-bold text-amber-600">{stats.reviews.flagged}</p>
        </div>
        <div className="bg-red-50 border border-red-200 rounded-xl p-5 text-center">
          <p className="text-xs text-gray-500 mb-1">Rejected</p>
          <p className="text-3xl font-bold text-red-600">{stats.reviews.rejected}</p>
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;