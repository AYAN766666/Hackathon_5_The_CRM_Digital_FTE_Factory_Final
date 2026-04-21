'use client';

/**
 * Analytics Dashboard Component
 * Displays sentiment analysis, trends, and metrics
 */
import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';
import {
  TrendingUp,
  TrendingDown,
  Activity,
  MessageSquare,
  ThumbsUp,
  Clock,
  RefreshCw,
  AlertTriangle,
  CheckCircle,
  BarChart3,
  Smile,
  Frown,
  Meh
} from 'lucide-react';
import { getAnalytics, APIError } from '@/lib/api';

interface AnalyticsData {
  total_tickets: number;
  active_tickets: number;
  escalated_tickets: number;
  closed_tickets: number;
  average_sentiment: number | null;
  sentiment_trend: Array<{
    date: string;
    average_sentiment: number;
    total_messages: number;
    positive_count: number;
    neutral_count: number;
    negative_count: number;
  }>;
  category_breakdown: Array<{
    category: string;
    count: number;
    percentage: number;
    average_sentiment: number | null;
  }>;
  channel_breakdown: Array<{
    channel: string;
    count: number;
    percentage: number;
    average_sentiment: number | null;
  }>;
  satisfaction_score: number;
  response_time_avg_ms: number | null;
}

const COLORS = ['#4F8DF7', '#28A745', '#FFC107', '#DC3545', '#6F42C1', '#FD7E14'];

export default function AnalyticsDashboard() {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalytics = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getAnalytics();
      setAnalytics(data);
    } catch (err: any) {
      // Extract user-friendly error message
      let errorMessage = 'Failed to load analytics';

      if (err instanceof APIError) {
        errorMessage = err.message;
        if (err.hint) {
          errorMessage += ` ${err.hint}`;
        }
      } else if (err.userMessage) {
        errorMessage = err.userMessage;
      } else if (err.message) {
        errorMessage = err.message;
      }

      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const getSentimentEmoji = (score: number | null) => {
    if (score === null) return <Meh className="w-5 h-5" />;
    if (score > 0.2) return <Smile className="w-5 h-5 text-green-600" />;
    if (score < -0.2) return <Frown className="w-5 h-5 text-red-600" />;
    return <Meh className="w-5 h-5 text-yellow-600" />;
  };

  const getSentimentColor = (score: number | null) => {
    if (score === null) return 'text-gray-600';
    if (score > 0.2) return 'text-green-600';
    if (score < -0.2) return 'text-red-600';
    return 'text-yellow-600';
  };

  const getSentimentBg = (score: number | null) => {
    if (score === null) return 'bg-gray-100';
    if (score > 0.2) return 'bg-green-100';
    if (score < -0.2) return 'bg-red-100';
    return 'bg-yellow-100';
  };

  return (
    <div className="w-full max-w-7xl mx-auto p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-8 p-6 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl shadow-lg">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-white/20 backdrop-blur-sm rounded-lg">
            <BarChart3 className="w-8 h-8 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white">Analytics Dashboard</h2>
            <p className="text-sm text-white/90">Sentiment analysis and performance metrics</p>
          </div>
        </div>
        <button
          onClick={fetchAnalytics}
          disabled={isLoading}
          className="flex items-center gap-2 px-4 py-2 bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white rounded-lg transition-all disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      {error && (
        <div
          className="mb-6 p-4 bg-red-50 border-2 border-red-200 rounded-lg flex items-center gap-3"
        >
          <AlertTriangle className="w-6 h-6 text-red-600" />
          <p className="text-red-800 font-semibold">{error}</p>
        </div>
      )}

      {!analytics && !isLoading && !error && (
        <div className="text-center py-12">
          <BarChart3 className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500">No analytics data available yet</p>
        </div>
      )}

      {analytics && (
        <>
          {/* Key Metrics Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <MetricCard
              title="Total Tickets"
              value={analytics.total_tickets}
              icon={<MessageSquare className="w-6 h-6" />}
              color="from-blue-500 to-purple-600"
            />
            <MetricCard
              title="Active Tickets"
              value={analytics.active_tickets}
              icon={<Activity className="w-6 h-6" />}
              color="from-green-500 to-emerald-600"
            />
            <MetricCard
              title="Escalated"
              value={analytics.escalated_tickets}
              icon={<AlertTriangle className="w-6 h-6" />}
              color="from-red-500 to-orange-600"
            />
            <MetricCard
              title="Satisfaction Score"
              value={`${analytics.satisfaction_score}%`}
              icon={<ThumbsUp className="w-6 h-6" />}
              color="from-yellow-500 to-pink-600"
            />
          </div>

          {/* Sentiment Trend Chart */}
          <div
            className="card-3d p-6 mb-8"
          >
            <div className="flex items-center gap-3 mb-4">
              <div className={`p-2 rounded-lg ${getSentimentBg(analytics.average_sentiment)}`}>
                {getSentimentEmoji(analytics.average_sentiment)}
              </div>
              <div>
                <h3 className="text-lg font-bold text-gray-900">Sentiment Trend (Last 7 Days)</h3>
                <p className="text-sm text-gray-500">
                  Average Sentiment: <span className={`font-bold ${getSentimentColor(analytics.average_sentiment)}`}>
                    {analytics.average_sentiment?.toFixed(3) || 'N/A'}
                  </span>
                </p>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={analytics.sentiment_trend}>
                <defs>
                  <linearGradient id="colorSentiment" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#4F8DF7" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#4F8DF7" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis domain={[-1, 1]} />
                <Tooltip />
                <Legend />
                <Area 
                  type="monotone" 
                  dataKey="average_sentiment"
                  stroke="#4F8DF7"
                  fillOpacity={1}
                  fill="url(#colorSentiment)"
                  name="Avg Sentiment"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          {/* Category and Channel Breakdown */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            {/* Category Breakdown */}
            <div
              className="card-3d p-6"
            >
              <h3 className="text-lg font-bold text-gray-900 mb-4">Category Breakdown</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={analytics.category_breakdown}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }: any) => `${name}: ${(percent! * 100).toFixed(1)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="count"
                  >
                    {analytics.category_breakdown.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* Channel Breakdown */}
            <div
              className="card-3d p-6"
            >
              <h3 className="text-lg font-bold text-gray-900 mb-4">Channel Distribution</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={analytics.channel_breakdown}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="channel" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="count" fill="#4F8DF7" name="Tickets" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Sentiment Distribution */}
          <div
            className="card-3d p-6 mb-8"
          >
            <h3 className="text-lg font-bold text-gray-900 mb-4">Sentiment Distribution (Last 7 Days)</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {analytics.sentiment_trend.map((day, index) => (
                <div key={index} className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm font-semibold text-gray-700 mb-2">{day.date}</p>
                  <div className="flex items-center gap-2 text-xs">
                    <span className="flex items-center gap-1 text-green-600">
                      <ThumbsUp className="w-3 h-3" />
                      {day.positive_count}
                    </span>
                    <span className="flex items-center gap-1 text-gray-600">
                      <Meh className="w-3 h-3" />
                      {day.neutral_count}
                    </span>
                    <span className="flex items-center gap-1 text-red-600">
                      <Frown className="w-3 h-3" />
                      {day.negative_count}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Performance Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Response Time */}
            <div
              className="card-3d p-6"
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg">
                  <Clock className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-900">Average Response Time</h3>
                  <p className="text-sm text-gray-500">AI processing latency</p>
                </div>
              </div>
              <div className="text-4xl font-bold text-gray-900">
                {analytics.response_time_avg_ms ? `${analytics.response_time_avg_ms}ms` : 'N/A'}
              </div>
              {analytics.response_time_avg_ms && analytics.response_time_avg_ms < 3000 && (
                <div className="mt-2 flex items-center gap-2 text-green-600">
                  <TrendingDown className="w-5 h-5" />
                  <span className="text-sm font-medium">Excellent performance!</span>
                </div>
              )}
            </div>

            {/* Overall Sentiment */}
            <div
              className="card-3d p-6"
            >
              <div className="flex items-center gap-3 mb-4">
                <div className={`p-2 rounded-lg ${getSentimentBg(analytics.average_sentiment)}`}>
                  {getSentimentEmoji(analytics.average_sentiment)}
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-900">Overall Sentiment</h3>
                  <p className="text-sm text-gray-500">Across all conversations</p>
                </div>
              </div>
              <div className={`text-4xl font-bold ${getSentimentColor(analytics.average_sentiment)}`}>
                {analytics.average_sentiment?.toFixed(3) || 'N/A'}
              </div>
              <div className="mt-2 text-sm text-gray-600">
                Scale: -1 (Very Negative) to +1 (Very Positive)
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

// Metric Card Component
function MetricCard({
  title,
  value,
  icon,
  color,
}: {
  title: string;
  value: number | string;
  icon: React.ReactNode;
  color: string;
}) {
  return (
    <div>
      <div className="card-3d p-6 bg-white dark:bg-gray-800 shadow-xl rounded-xl">
        <div className="flex items-center justify-between mb-4">
          <div className={`p-3 rounded-lg bg-gradient-to-r ${color} text-white shadow-lg`}>
            {icon}
          </div>
        </div>
        <p className="text-sm text-gray-600 dark:text-gray-300 mb-1">{title}</p>
        <p className="text-3xl font-bold text-gray-900 dark:text-white">{value}</p>
      </div>
    </div>
  );
}
