import React, { useState, useEffect } from "react";
import axios from "axios";

const API = "http://localhost:5000/api";

function ProductDetail({ productId, addToCart, onBack, currentPersona }) {
  const [product, setProduct] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [reviewText, setReviewText] = useState("");
  const [reviewRating, setReviewRating] = useState(0);
  const [reviewName, setReviewName] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchProduct();
  }, [productId]);

  // Auto fill reviewer name from the active persona
  useEffect(() => {
    if (currentPersona && currentPersona.id !== "guest") {
      setReviewName(currentPersona.name);
    } else {
      setReviewName("");
    }
  }, [currentPersona]);

  const fetchProduct = async () => {
    try {
      const res = await axios.get(`${API}/products/${productId}`);
      setProduct(res.data.product);
      setReviews(res.data.reviews);
    } catch (err) {
      console.error(err);
    }
  };

  const submitReview = async () => {
    if (!reviewText.trim() || reviewRating === 0) return;
    setSubmitting(true);
    setMessage("");

    try {
      const res = await axios.post(`${API}/reviews`, {
        product_id: productId,
        customer_name: reviewName || "Anonymous",
        rating: reviewRating,
        text: reviewText,
      });

      setMessage(res.data.message);
      setReviewText("");
      setReviewRating(0);
      fetchProduct();
    } catch (err) {
      setMessage("Failed to submit review.");
    }
    setSubmitting(false);
  };

  if (!product) {
    return <div className="text-center py-20 text-gray-500">Loading...</div>;
  }

  const isPersona = currentPersona && currentPersona.id !== "guest";

  return (
    <div>
      <button
        onClick={onBack}
        className="text-sm text-indigo-600 hover:text-indigo-700 mb-6 font-medium"
      >
        Back to Store
      </button>

      <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Image */}
          <div className="bg-gray-50 rounded-xl flex items-center justify-center p-8">
            <img
              src={product.image}
              alt={product.name}
              className="max-h-72 max-w-full object-contain"
              onError={(e) => {
                e.target.style.display = "none";
              }}
            />
          </div>

          {/* Info */}
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              {product.name}
            </h2>
            <p className="text-sm text-gray-500 mb-4">
              {product.brand}, {product.category}
            </p>
            <p className="text-gray-600 mb-4">{product.description}</p>

            <div className="flex items-center gap-3 mb-4">
              <span className="text-3xl font-bold text-gray-900">
                ${product.price}
              </span>
              <span
                className={`text-xs px-3 py-1 rounded-full font-medium ${
                  product.age_rating.includes("18") ||
                  product.age_rating.includes("17")
                    ? "bg-red-100 text-red-700"
                    : "bg-emerald-100 text-emerald-700"
                }`}
              >
                {product.age_rating}
              </span>
              <span
                className={`text-sm font-medium ${
                  product.in_stock ? "text-emerald-600" : "text-red-500"
                }`}
              >
                {product.in_stock ? "In Stock" : "Out of Stock"}
              </span>
            </div>

            {/* Specs */}
            <div className="bg-gray-50 rounded-lg p-4 mb-4">
              <h3 className="text-sm font-semibold text-gray-700 mb-2">
                Specifications
              </h3>
              {Object.entries(product.specs).map(([key, val]) => (
                <div key={key} className="flex justify-between text-sm py-1">
                  <span className="text-gray-500">
                    {key
                      .replace(/_/g, " ")
                      .replace(/\b\w/g, (c) => c.toUpperCase())}
                  </span>
                  <span className="text-gray-800 font-medium">
                    {Array.isArray(val) ? val.join(", ") : val}
                  </span>
                </div>
              ))}
            </div>

            <button
              onClick={() => addToCart(product)}
              disabled={!product.in_stock}
              className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 text-white py-3 rounded-lg font-medium transition-colors"
            >
              {product.in_stock ? "Add to Cart" : "Out of Stock"}
            </button>
          </div>
        </div>
      </div>

      {/* Reviews Section */}
      <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Customer Reviews ({reviews.length})
        </h3>

        {reviews.length === 0 ? (
          <p className="text-gray-500 text-sm">
            No reviews yet. Be the first to review!
          </p>
        ) : (
          <div className="space-y-4 mb-6">
            {reviews.map((review) => (
              <div key={review.id} className="border-b border-gray-100 pb-4">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-medium text-sm text-gray-900">
                    {review.customer_name}
                  </span>
                  <span className="text-xs text-gray-400">
                    {review.timestamp}
                  </span>
                </div>
                <div className="flex gap-1 mb-2">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <span
                      key={star}
                      className={`text-sm ${
                        star <= review.rating
                          ? "text-amber-400"
                          : "text-gray-300"
                      }`}
                    >
                      *
                    </span>
                  ))}
                </div>
                <p className="text-sm text-gray-600">{review.text}</p>
              </div>
            ))}
          </div>
        )}

        {/* Write Review */}
        <div className="border-t border-gray-100 pt-4">
          <h4 className="text-sm font-semibold text-gray-900 mb-3">
            Write a Review
          </h4>

          {isPersona && (
            <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-3 mb-3 text-sm">
              <p className="text-indigo-700">
                Posting as{" "}
                <span className="font-semibold">{currentPersona.name}</span>.
                The AI will check this reviewer's past history.
              </p>
            </div>
          )}

          {message && (
            <div
              className={`mb-3 p-3 rounded-lg text-sm ${
                message.includes("Thank")
                  ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                  : "bg-amber-50 text-amber-700 border border-amber-200"
              }`}
            >
              {message}
            </div>
          )}

          <input
            type="text"
            placeholder="Your name (optional)"
            value={reviewName}
            onChange={(e) => setReviewName(e.target.value)}
            className="w-full bg-gray-50 border border-gray-300 rounded-lg px-4 py-2 text-sm mb-3 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />

          <div className="flex items-center gap-2 mb-3">
            <span className="text-sm text-gray-600">Rating:</span>
            {[1, 2, 3, 4, 5].map((star) => (
              <button
                key={star}
                onClick={() => setReviewRating(star)}
                className={`text-lg ${
                  reviewRating >= star ? "text-amber-400" : "text-gray-300"
                }`}
              >
                *
              </button>
            ))}
            {reviewRating === 0 && (
              <span className="text-xs text-gray-400 ml-1">
                Select a rating
              </span>
            )}
          </div>

          <textarea
            placeholder="Write your review..."
            value={reviewText}
            onChange={(e) => setReviewText(e.target.value)}
            rows={3}
            className="w-full bg-gray-50 border border-gray-300 rounded-lg px-4 py-2 text-sm mb-3 resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />

          <button
            onClick={submitReview}
            disabled={submitting || !reviewText.trim() || reviewRating === 0}
            className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 text-white px-6 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            {submitting ? "Submitting..." : "Submit Review"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default ProductDetail;
