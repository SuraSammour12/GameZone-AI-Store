import React, { useState, useEffect } from "react";
import axios from "axios";

const API = "http://localhost:5000/api";

function InvoicesPanel() {
  const [invoices, setInvoices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchInvoices();
  }, []);

  const fetchInvoices = async () => {
    try {
      const res = await axios.get(`${API}/invoices`);
      setInvoices(res.data.invoices);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  const markPaid = async (invoiceId) => {
    try {
      await axios.post(`${API}/invoices/${invoiceId}/pay`);
      fetchInvoices();
    } catch (err) {
      console.error(err);
    }
  };

  const openPdf = (invoiceId) => {
    window.open(`${API}/invoices/${invoiceId}/pdf`, "_blank");
  };

  if (loading) {
    return <div className="text-center py-20 text-gray-500">Loading...</div>;
  }

  if (invoices.length === 0) {
    return (
      <div className="bg-white border border-gray-200 rounded-xl p-12 text-center shadow-sm">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">No Invoices Yet</h3>
        <p className="text-gray-500 text-sm">
          Invoices are generated automatically when an order is approved.
        </p>
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">
          Invoices ({invoices.length})
        </h2>
        <button
          onClick={fetchInvoices}
          className="text-sm text-indigo-600 hover:text-indigo-700 font-medium"
        >
          Refresh
        </button>
      </div>

      <div className="bg-white border border-gray-200 rounded-xl divide-y divide-gray-100 shadow-sm">
        {invoices.map((inv) => (
          <div key={inv.id} className="p-4 flex items-center gap-4">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-3">
                <span className="font-semibold text-gray-900">{inv.id}</span>
                <span
                  className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                    inv.status === "paid"
                      ? "bg-emerald-100 text-emerald-700"
                      : "bg-amber-100 text-amber-700"
                  }`}
                >
                  {inv.status}
                </span>
              </div>
              <p className="text-xs text-gray-500 mt-1">
                {inv.customer_name} &middot; Order {inv.order_id} &middot; {inv.issued_at}
              </p>
            </div>

            <span className="font-bold text-gray-900">${inv.total}</span>

            <button
              onClick={() => openPdf(inv.id)}
              className="px-4 py-2 rounded-lg text-sm font-medium bg-white text-indigo-600 border border-indigo-300 hover:bg-indigo-50 transition-colors"
            >
              View PDF
            </button>

            {inv.status !== "paid" && (
              <button
                onClick={() => markPaid(inv.id)}
                className="px-4 py-2 rounded-lg text-sm font-medium bg-emerald-600 text-white hover:bg-emerald-700 transition-colors"
              >
                Mark Paid
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default InvoicesPanel;
