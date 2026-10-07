import React from "react";

function Cart({ cart, removeFromCart, onCheckout, currentPersona }) {
  const subtotal = cart.reduce(
    (sum, item) => sum + item.product.price * item.quantity,
    0
  );
  const shipping = subtotal >= 100 ? 0 : 5;
  const total = subtotal + shipping;

  if (cart.length === 0) {
    return (
      <div className="bg-white border border-gray-200 rounded-xl p-12 text-center shadow-sm">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          Your Cart is Empty
        </h3>
        <p className="text-gray-500 text-sm">
          Browse the store and add some games!
        </p>
      </div>
    );
  }

  const isPersona = currentPersona && currentPersona.id !== "guest";

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Cart Items */}
      <div className="lg:col-span-2 space-y-3">
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-lg font-semibold text-gray-900">
            Shopping Cart ({cart.length} items)
          </h2>
          {isPersona && (
            <span className="text-xs text-gray-500">
              Shopping as{" "}
              <span className="font-medium text-gray-700">
                {currentPersona.name}
              </span>
            </span>
          )}
        </div>
        {cart.map((item) => (
          <div
            key={item.product.id}
            className="bg-white border border-gray-200 rounded-xl p-4 flex items-center gap-4 shadow-sm"
          >
            <div className="w-20 h-20 bg-gray-50 rounded-lg flex items-center justify-center flex-shrink-0">
              <img
                src={item.product.image}
                alt={item.product.name}
                className="max-h-full max-w-full object-contain p-2"
                onError={(e) => {
                  e.target.style.display = "none";
                }}
              />
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="font-semibold text-gray-900 text-sm">
                {item.product.name}
              </h3>
              <p className="text-xs text-gray-500">{item.product.brand}</p>
              <p className="text-sm font-bold text-gray-900 mt-1">
                ${item.product.price} x {item.quantity} = $
                {item.product.price * item.quantity}
              </p>
            </div>
            <button
              onClick={() => removeFromCart(item.product.id)}
              className="text-sm text-red-500 hover:text-red-700 font-medium"
            >
              Remove
            </button>
          </div>
        ))}
      </div>

      {/* Summary */}
      <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm h-fit">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Order Summary
        </h3>
        <div className="space-y-2 text-sm mb-4">
          <div className="flex justify-between">
            <span className="text-gray-500">Subtotal</span>
            <span className="text-gray-900">${subtotal}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-500">Shipping</span>
            <span
              className={
                shipping === 0
                  ? "text-emerald-600 font-medium"
                  : "text-gray-900"
              }
            >
              {shipping === 0 ? "Free" : `$${shipping}`}
            </span>
          </div>
          <div className="border-t border-gray-100 pt-2 flex justify-between">
            <span className="font-semibold text-gray-900">Total</span>
            <span className="font-bold text-lg text-gray-900">${total}</span>
          </div>
        </div>
        <p className="text-xs text-gray-500 mb-4">Payment: Cash on delivery</p>
        <button
          onClick={onCheckout}
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-lg font-medium transition-colors"
        >
          Proceed to Checkout
        </button>
      </div>
    </div>
  );
}

export default Cart;
