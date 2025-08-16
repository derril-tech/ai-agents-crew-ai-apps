import React from 'react';

interface Review {
  id: string;
  title: string;
  status: 'pending' | 'completed' | 'error';
  score: number;
  suggestions: string[];
}

interface Props {
  reviews: Review[];
  loading: boolean;
}

export default function CodeReviewDashboard({ reviews, loading }: Props) {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-2 text-gray-600">Loading reviews...</span>
      </div>
    );
  }
  
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-gray-900">Code Reviews</h2>
        <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
          New Review
        </button>
      </div>
      
      <div className="grid gap-4">
        {reviews.map((review) => (
          <div key={review.id} className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex justify-between items-start">
              <h3 className="text-lg font-medium text-gray-900">{review.title}</h3>
              <span className="px-2 py-1 rounded-full text-sm bg-gray-100 text-gray-800">
                {review.status}
              </span>
            </div>
            <div className="mt-2">
              <span className="text-sm text-gray-600">Score: {review.score}/100</span>
            </div>
            {review.suggestions.length > 0 && (
              <div className="mt-4">
                <h4 className="text-sm font-medium text-gray-900 mb-2">Suggestions:</h4>
                <ul className="space-y-1">
                  {review.suggestions.map((suggestion, index) => (
                    <li key={index} className="text-sm text-gray-600">• {suggestion}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}