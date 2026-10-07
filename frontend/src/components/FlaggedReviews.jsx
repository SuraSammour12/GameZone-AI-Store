import React, { useState, useEffect } from "react";
import axios from "axios";

const API = "http://localhost:5000/api";

function FlaggedReviews() {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReviews();
  }, []);

  const fetchReviews = async () => {
    try {
      const res = await axios.get(`${API}/reviews?status=flagged`);
      setReviews(res.data.reviews);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  const handleDecision = async (reviewId, action) => {
    try {
      await axios.post(`${API}/reviews/${reviewId}/decide`, {
        action,
        note: action === "reject" ? "Rejected by admin" : "Published after review",
      });
      fetchReviews();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return <div className="text-center py-20 text-gray-500">Loading...</div>;
  }

  if (reviews.length === 0) {
    return (
      <div className="bg-white border border-gray-200 rounded-xl p-12 text-center shadow-sm">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">No Flagged Reviews</h3>
        <p className="text-gray-500 text-sm">All reviews are clean. The AI is monitoring.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold text-gray-900">
        Flagged Reviews ({reviews.length})
      </h2>

      {reviews.map((review) => (
        <div
          key={review.id}
          className="bg-white border border-amber-200 rounded-xl p-5 shadow-sm"
        >
          <div className="flex items-center justify-between mb-3">
            <div>
              <span className="font-semibold text-gray-900">{review.id}</span>
              <span className="text-sm text-gray-500 ml-3">by {review.customer_name}</span>
            </div>
            {review.ai_analysis && (
              <span className={`text-xs px-3 py-1 rounded-full font-medium ${
                review.ai_analysis.toxicity_level === "high"
                  ? "bg-red-100 text-red-700"
                  : review.ai_analysis.toxicity_level === "medium"
                  ? "bg-amber-100 text-amber-700"
                  : "bg-gray-100 text-gray-700"
              }`}>
                Toxicity: {review.ai_analysis.toxicity_level}
              </span>
            )}
          </div>

          {/* The Review */}
          <div className="bg-gray-50 rounded-lg p-4 mb-4">
            <div className="flex gap-1 mb-2">
              {[1, 2, 3, 4, 5].map((star) => (
                <span key={star} className={`text-sm ${star <= review.rating ? "text-amber-400" : "text-gray-300"}`}>
                  *
                </span>
              ))}
            </div>
            <p className="text-sm text-gray-800">{review.text}</p>
          </div>

          {/* AI Analysis */}
          {review.ai_analysis && (
            <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-4">
              <p className="text-sm font-semibold text-amber-700 mb-1">AI Analysis:</p>
              <p className="text-sm text-amber-600 mb-1">{review.ai_analysis.reason}</p>
              <p className="text-xs text-gray-600">Category: {review.ai_analysis.category}</p>
            </div>
          )}

          <div className="flex gap-3 justify-end">
            <button
              onClick={() => handleDecision(review.id, "reject")}
              className="px-5 py-2 rounded-lg text-sm font-medium bg-white text-red-600 border border-red-300 hover:bg-red-50 transition-colors"
            >
              Reject
            </button>
            <button
              onClick={() => handleDecision(review.id, "publish")}
              className="px-5 py-2 rounded-lg text-sm font-medium bg-emerald-600 text-white hover:bg-emerald-700 transition-colors"
            >
              Publish
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default FlaggedReviews;