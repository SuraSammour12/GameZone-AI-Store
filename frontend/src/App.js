import React, { useState, useEffect } from "react";
import StoreFront from "./components/StoreFront";
import ProductDetail from "./components/ProductDetail";
import Cart from "./components/Cart";
import Checkout from "./components/Checkout";
import AdminDashboard from "./components/AdminDashboard";
import FlaggedOrders from "./components/FlaggedOrders";
import FlaggedReviews from "./components/FlaggedReviews";
import InvoicesPanel from "./components/InvoicesPanel";
import ActivityLog from "./components/ActivityLog";
import CustomerSwitcher from "./components/CustomerSwitcher";
import { GUEST_CUSTOMER, getPersonaById } from "./data/personas";

const CUSTOMER_TABS = [
  { id: "store", label: "Store" },
  { id: "cart", label: "Cart" },
];

const ADMIN_TABS = [
  { id: "dashboard", label: "Dashboard" },
  { id: "flagged-orders", label: "Flagged Orders" },
  { id: "flagged-reviews", label: "Flagged Reviews" },
  { id: "invoices", label: "Invoices" },
  { id: "activity", label: "Activity Log" },
];

const PERSONA_STORAGE_KEY = "gamezone_active_persona";

function App() {
  const [mode, setMode] = useState("customer");
  const [activeTab, setActiveTab] = useState("store");
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [cart, setCart] = useState([]);
  const [currentPersona, setCurrentPersona] = useState(GUEST_CUSTOMER);

  useEffect(() => {
    try {
      const savedId = localStorage.getItem(PERSONA_STORAGE_KEY);
      if (savedId) {
        setCurrentPersona(getPersonaById(savedId));
      }
    } catch (e) {
      // localStorage may be unavailable, safe to ignore
    }
  }, []);

  const handlePersonaChange = (persona) => {
    setCurrentPersona(persona);
    try {
      localStorage.setItem(PERSONA_STORAGE_KEY, persona.id);
    } catch (e) {
      // ignore
    }
  };

  const addToCart = (product, quantity = 1) => {
    setCart((prev) => {
      const existing = prev.find((item) => item.product.id === product.id);
      if (existing) {
        return prev.map((item) =>
          item.product.id === product.id
            ? { ...item, quantity: item.quantity + quantity }
            : item
        );
      }
      return [...prev, { product, quantity }];
    });
  };

  const removeFromCart = (productId) => {
    setCart((prev) => prev.filter((item) => item.product.id !== productId));
  };

  const clearCart = () => setCart([]);

  const cartCount = cart.reduce((sum, item) => sum + item.quantity, 0);

  const switchMode = (newMode) => {
    setMode(newMode);
    setActiveTab(newMode === "customer" ? "store" : "dashboard");
    setSelectedProduct(null);
  };

  const tabs = mode === "customer" ? CUSTOMER_TABS : ADMIN_TABS;

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 tracking-tight">
              GameZone
            </h1>
            <p className="text-sm text-gray-500">
              {mode === "customer"
                ? "Your favorite gaming store"
                : "Admin Panel, AI Monitoring"}
            </p>
          </div>
          <div className="flex items-center gap-3">
            {mode === "customer" && (
              <CustomerSwitcher
                currentPersona={currentPersona}
                onSelect={handlePersonaChange}
              />
            )}
            {mode === "customer" && (
              <button
                onClick={() => {
                  setActiveTab("cart");
                  setSelectedProduct(null);
                }}
                className="relative text-sm text-gray-600 hover:text-gray-900 px-2"
              >
                Cart
                {cartCount > 0 && (
                  <span className="absolute -top-2 -right-1 bg-red-500 text-white text-xs w-5 h-5 rounded-full flex items-center justify-center">
                    {cartCount}
                  </span>
                )}
              </button>
            )}
            <button
              onClick={() =>
                switchMode(mode === "customer" ? "admin" : "customer")
              }
              className="text-sm px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors"
            >
              {mode === "customer" ? "Switch to Admin" : "Switch to Store"}
            </button>
          </div>
        </div>

        {/* Tabs */}
        <nav className="max-w-7xl mx-auto px-6 flex gap-1 border-t border-gray-100">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => {
                setActiveTab(tab.id);
                setSelectedProduct(null);
              }}
              className={`px-5 py-3 text-sm font-medium transition-colors ${
                activeTab === tab.id
                  ? "text-indigo-600 border-b-2 border-indigo-600"
                  : "text-gray-500 hover:text-gray-800"
              }`}
            >
              {tab.label}
              {tab.id === "cart" && cartCount > 0 && (
                <span className="ml-2 bg-red-100 text-red-600 text-xs px-2 py-0.5 rounded-full">
                  {cartCount}
                </span>
              )}
            </button>
          ))}
        </nav>
      </header>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-6 py-6">
        {/* Customer Views */}
        {mode === "customer" && activeTab === "store" && !selectedProduct && (
          <StoreFront
            onSelectProduct={setSelectedProduct}
            addToCart={addToCart}
          />
        )}
        {mode === "customer" && selectedProduct && (
          <ProductDetail
            productId={selectedProduct}
            addToCart={addToCart}
            onBack={() => setSelectedProduct(null)}
            currentPersona={currentPersona}
          />
        )}
        {mode === "customer" && activeTab === "cart" && (
          <Cart
            cart={cart}
            removeFromCart={removeFromCart}
            onCheckout={() => setActiveTab("checkout")}
            currentPersona={currentPersona}
          />
        )}
        {mode === "customer" && activeTab === "checkout" && (
          <Checkout
            cart={cart}
            clearCart={clearCart}
            onDone={() => setActiveTab("store")}
            currentPersona={currentPersona}
          />
        )}

        {/* Admin Views */}
        {mode === "admin" && activeTab === "dashboard" && <AdminDashboard />}
        {mode === "admin" && activeTab === "flagged-orders" && <FlaggedOrders />}
        {mode === "admin" && activeTab === "flagged-reviews" && <FlaggedReviews />}
        {mode === "admin" && activeTab === "invoices" && <InvoicesPanel />}
        {mode === "admin" && activeTab === "activity" && <ActivityLog />}
      </main>
    </div>
  );
}

export default App;
