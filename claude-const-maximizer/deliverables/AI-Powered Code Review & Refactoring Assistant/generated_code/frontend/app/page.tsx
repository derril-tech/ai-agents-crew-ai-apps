'use client';

import React, { useState, useEffect } from 'react';
import CodeReviewDashboard from '../components/CodeReviewDashboard';
import Header from '../components/Header';

export default function CodeReviewPage() {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Fetch code reviews from API
    fetch('/api/reviews')
      .then(res => res.json())
      .then(data => {
        setReviews(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching reviews:', err);
        setLoading(false);
      });
  }, []);
  
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <CodeReviewDashboard reviews={reviews} loading={loading} />
      </main>
    </div>
  );
}