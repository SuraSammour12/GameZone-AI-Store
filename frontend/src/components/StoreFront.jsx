import React, { useState, useEffect } from "react";
import axios from "axios";

const API = "http://localhost:5000/api";

function StoreFront({ onSelectProduct, addToCart }) {
  const [products, setProducts] = useState([]);
  const [filter, setFilter] = useState("All");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const res = await axios.get(`${API}/products`);
      setProducts(res.data.products);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  const categories = ["All", ...new Set(products.map((p) => p.category))];
  const filtered = filter === "All" ? products : products.filter((p) => p.category === filter);

  if (loading) {
    return <div className="text-center py-20 text-gray-500">Loading products...</div>;
  }

  return (
    <div>
      {/* Category Filter */}
      <div className="flex gap-2 mb-6 flex-wrap">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setFilter(cat)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filter === cat
                ? "bg-indigo-600 text-white"
                : "bg-white border border-gray-300 text-gray-600 hover:bg-gray-50"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Product Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
        {filtered.map((product) => (
          <div
            key={product.id}
            className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow"
          >
            {/* Image */}
            <div
              className="h-48 bg-gray-100 flex items-center justify-center p-4 cursor-pointer"
              onClick={() => onSelectProduct(product.id)}
            >
              <img
                src={product.image}
                alt={product.name}
                className="max-h-full max-w-full object-contain"
                onError={(e) => {
                  e.target.style.display = "none";
                  e.target.parentNode.innerHTML =
                    '<div class="text-gray-400 text-sm">Image not available</div>';
                }}
              />
            </div>

            {/* Info */}
            <div className="p-4">
              <div className="flex items-start justify-between mb-1">
                <h3
                  className="font-semibold text-gray-900 text-sm cursor-pointer hover:text-indigo-600"
                  onClick={() => onSelectProduct(product.id)}
                >
                  {product.name}
                </h3>
              </div>
              <p className="text-xs text-gray-500 mb-2">{product.brand}</p>
              <div className="flex items-center gap-2 mb-3">
                <span className="text-lg font-bold text-gray-900">${product.price}</span>
                <span
                  className={`text-xs px-2 py-0.5 rounded-full ${
                    product.age_rating.includes("18") || product.age_rating.includes("17")
                      ? "bg-red-100 text-red-700"
                      : "bg-emerald-100 text-emerald-700"
                  }`}
                >
                  {product.age_rating}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span
                  className={`text-xs font-medium ${
                    product.in_stock ? "text-emerald-600" : "text-red-500"
                  }`}
                >
                  {product.in_stock ? "In Stock" : "Out of Stock"}
                </span>
                <button
                  onClick={() => addToCart(product)}
                  disabled={!product.in_stock}
                  className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 text-white text-xs px-4 py-2 rounded-lg font-medium transition-colors"
                >
                  Add to Cart
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default StoreFront;