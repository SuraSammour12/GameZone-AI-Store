import React, { useState, useEffect } from "react";
import axios from "axios";

const API = "http://localhost:5000/api";

function Checkout({ cart, clearCart, onDone, currentPersona }) {
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [address, setAddress] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);

  // Auto fill from the active persona so the agent recognises the buyer
  useEffect(() => {
    if (currentPersona && currentPersona.id !== "guest") {
      setName(currentPersona.name);
      setPhone(currentPersona.phone);
      setAddress(currentPersona.address);
    } else {
      setName("");
      setPhone("");
      setAddress("");
    }
  }, [currentPersona]);

  const subtotal = cart.reduce(
    (sum, item) => sum + item.product.price * item.quantity,
    0
  );
  const shipping = subtotal >= 100 ? 0 : 5;
  const total = subtotal + shipping;

  const placeOrder = async () => {
    if (!name.trim() || !address.trim()) return;
    setSubmitting(true);

    try {
      const res = await axios.post(`${API}/orders`, {
        customer_name: name,
        customer_phone: phone,
        customer_address: address,
        items: cart.map((item) => ({
          product_id: item.product.id,
          quantity: item.quantity,
        })),
      });
      setResult(res.data);
      clearCart();
    } catch (err) {
      setResult({ message: "Failed to place order. Please try again." });
    }
    setSubmitting(false);
  };

  if (result) {
    const order = result.order;
    const isApproved = order && order.status === "approved";

    return (
      <div className="bg-white border border-gray-200 rounded-xl p-8 text-center shadow-sm max-w-lg mx-auto">
        <div
          className={`text-5xl mb-4 ${
            isApproved ? "text-emerald-500" : "text-amber-500"
          }`}
        >
          {isApproved ? "V" : "!"}
        </div>
        <h2 className="text-xl font-bold text-gray-900 mb-2">
          {isApproved ? "Order Confirmed!" : "Order Under Review"}
        </h2>
        <p className="text-gray-600 mb-4">{result.message}</p>
        {order && (
          <div className="bg-gray-50 rounded-lg p-4 text-sm text-left mb-4">
            <p>
              <span className="text-gray-500">Order ID:</span>{" "}
              <span className="font-semibold">{order.id}</span>
            </p>
            <p>
              <span className="text-gray-500">Total:</span>{" "}
              <span className="font-semibold">${order.total}</span>
            </p>
            <p>
              <span className="text-gray-500">Payment:</span>{" "}
              <span className="font-semibold">Cash on delivery</span>
            </p>
            <p>
              <span className="text-gray-500">Status:</span>
              <span
                className={`font-semibold ml-1 ${
                  isApproved ? "text-emerald-600" : "text-amber-600"
                }`}
              >
                {order.status === "approved" ? "Approved" : "Under Review"}
              </span>
            </p>
          </div>
        )}
        {!isApproved && order && order.ai_analysis && (
          <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 text-sm text-left mb-4">
            <p className="font-semibold text-amber-700 mb-1">AI Review Note:</p>
            <p className="text-amber-600">{order.ai_analysis.reason}</p>
          </div>
        )}
        <button
          onClick={onDone}
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          Continue Shopping
        </button>
      </div>
    );
  }

  const isPersona = currentPersona && currentPersona.id !== "guest";

  return (
    <div className="max-w-lg mx-auto">
      <h2 className="text-xl font-bold text-gray-900 mb-4">Checkout</h2>

      {isPersona && (
        <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-3 mb-4 text-sm">
          <p className="text-indigo-700">
            <span className="font-semibold">Ordering as {currentPersona.name}.</span>{" "}
            The AI agent will match this identity against past history when
            analyzing the order.
          </p>
        </div>
      )}

      <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm mb-6">
        <h3 className="text-sm font-semibold text-gray-900 mb-4">
          Delivery Information
        </h3>

        <div className="space-y-3">
          <div>
            <label className="text-xs text-gray-500 mb-1 block">
              Full Name *
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full bg-gray-50 border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <div>
            <label className="text-xs text-gray-500 mb-1 block">
              Phone Number
            </label>
            <input
              type="text"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="w-full bg-gray-50 border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <div>
            <label className="text-xs text-gray-500 mb-1 block">
              Delivery Address *
            </label>
            <textarea
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              rows={3}
              className="w-full bg-gray-50 border border-gray-300 rounded-lg px-4 py-2 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </div>
      </div>

      {/* Order Summary */}
      <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm mb-6">
        <h3 className="text-sm font-semibold text-gray-900 mb-3">
          Order Summary
        </h3>
        {cart.map((item) => (
          <div
            key={item.product.id}
            className="flex justify-between text-sm py-1"
          >
            <span className="text-gray-600">
              {item.product.name} x{item.quantity}
            </span>
            <span className="text-gray-900">
              ${item.product.price * item.quantity}
            </span>
          </div>
        ))}
        <div className="border-t border-gray-100 mt-2 pt-2 flex justify-between text-sm">
          <span className="text-gray-500">Shipping</span>
          <span>{shipping === 0 ? "Free" : `$${shipping}`}</span>
        </div>
        <div className="border-t border-gray-100 mt-2 pt-2 flex justify-between">
          <span className="font-semibold">Total</span>
          <span className="font-bold text-lg">${total}</span>
        </div>
        <p className="text-xs text-gray-500 mt-2">Payment: Cash on delivery</p>
      </div>

      <button
        onClick={placeOrder}
        disabled={submitting || !name.trim() || !address.trim()}
        className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 text-white py-3 rounded-lg font-medium transition-colors"
      >
        {submitting ? "Processing..." : `Place Order, $${total}`}
      </button>
    </div>
  );
}

export default Checkout;
