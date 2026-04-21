'use client';

/**
 * Home Page - Customer Support Portal
 * Enhanced with animations, live stats, and more!
 */
import React, { useState } from 'react';
import { motion } from 'framer-motion';
import SupportForm from '@/components/SupportForm';
import TicketStatusModal from '@/components/TicketStatusModal';
import ParticleBackground from '@/components/ParticleBackground';
import Confetti from '@/components/Confetti';
import ToastContainer, { useToast } from '@/components/ToastContainer';
import LiveStats from '@/components/LiveStats';
import ThemeToggle from '@/components/ThemeToggle';
import QuickActions from '@/components/QuickActions';
import AnalyticsDashboard from '@/components/AnalyticsDashboard';
import { Ticket, MessageSquare, Clock, Shield, Zap, Heart, Globe, BarChart3 } from 'lucide-react';

export default function Home() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isAnalyticsOpen, setIsAnalyticsOpen] = useState(false);
  const [lastTicketId, setLastTicketId] = useState<string | null>(null);
  const [showConfetti, setShowConfetti] = useState(false);
  const { toasts, removeToast, success, error, info } = useToast();

  const handleTicketCreated = (ticketId: string) => {
    setLastTicketId(ticketId);
    setShowConfetti(true);
    success(`Ticket ${ticketId} created successfully! 🎉`, 5000);
  };

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  const openAnalytics = () => {
    setIsAnalyticsOpen(true);
  };

  const closeAnalytics = () => {
    setIsAnalyticsOpen(false);
  };

  return (
    <div className="min-h-screen py-12 px-4 relative">
      {/* Particle Background */}
      <ParticleBackground />

      {/* Theme Toggle */}
      <ThemeToggle />

      {/* Confetti Animation */}
      <Confetti isActive={showConfetti} onComplete={() => setShowConfetti(false)} />

      {/* Toast Notifications */}
      <ToastContainer toasts={toasts} onRemove={removeToast} />

      {/* Theme Toggle */}
      <ThemeToggle />
      <div className="max-w-7xl mx-auto relative z-10">
        {/* Header Section */}
        <div className="text-center mb-8">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="flex items-center justify-center gap-3 mb-4">
              <motion.div
                animate={{ rotate: [0, 10, -10, 0] }}
                transition={{ duration: 2, repeat: Infinity, repeatDelay: 3 }}
              >
                <Zap className="w-12 h-12 text-yellow-300 drop-shadow-lg" />
              </motion.div>
              <h1 className="text-5xl font-bold text-white mb-0 drop-shadow-lg">
                Customer Support Portal
              </h1>
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 1.5, repeat: Infinity }}
              >
                <Heart className="w-12 h-12 text-red-300 drop-shadow-lg" />
              </motion.div>
            </div>
            <p className="text-xl text-white/90 max-w-2xl mx-auto">
              24/7 AI-powered multi-channel support system
            </p>
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.5, type: 'spring', stiffness: 200 }}
            >
              <div className="inline-flex items-center gap-2 mt-4 px-4 py-2 bg-white/20 backdrop-blur-sm rounded-full text-white">
                <Globe className="w-5 h-5" />
                <span className="text-sm font-medium">Serving customers worldwide 🌍</span>
              </div>
            </motion.div>
            
            {/* Trust Badges */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.8 }}
            >
              <div className="flex items-center justify-center gap-4 mt-6">
                <motion.div
                  whileHover={{ scale: 1.1, rotate: 5 }}
                >
                  <div className="px-4 py-2 bg-white/10 backdrop-blur-sm rounded-lg">
                    <p className="text-xs text-white/80">🔒 Secure</p>
                  </div>
                </motion.div>
                <motion.div
                  whileHover={{ scale: 1.1, rotate: -5 }}
                >
                  <div className="px-4 py-2 bg-white/10 backdrop-blur-sm rounded-lg">
                    <p className="text-xs text-white/80">⚡ Fast</p>
                  </div>
                </motion.div>
                <motion.div
                  whileHover={{ scale: 1.1, rotate: 5 }}
                >
                  <div className="px-4 py-2 bg-white/10 backdrop-blur-sm rounded-lg">
                    <p className="text-xs text-white/80">🤖 AI-Powered</p>
                  </div>
                </motion.div>
              </div>
            </motion.div>
          </motion.div>
        </div>

        {/* Live Statistics Dashboard */}
        <LiveStats />

        {/* Live Visitor Badge */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <div className="text-center mb-8">
            <div className="inline-flex items-center gap-3 px-6 py-3 bg-white/20 backdrop-blur-md rounded-full shadow-lg">
            <div className="flex -space-x-2">
              {[1, 2, 3].map((i) => (
                <motion.div
                  key={i}
                  animate={{ y: [0, -5, 0] }}
                  transition={{ duration: 1.5, repeat: Infinity, delay: i * 0.2 }}
                >
                  <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-400 to-purple-500 border-2 border-white flex items-center justify-center text-white text-xs font-bold">
                    👤
                  </div>
                </motion.div>
              ))}
            </div>
            <div className="text-white">
              <p className="text-sm font-bold">
                <motion.span
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ duration: 2, repeat: Infinity }}
                >
                  247
                </motion.span>
                {' '}users online
              </p>
              <p className="text-xs text-white/80">Active now</p>
            </div>
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
            >
              🔄
            </motion.div>
            </div>
          </div>
        </motion.div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12 max-w-4xl mx-auto">
          <FeatureCard
            icon={<MessageSquare className="w-8 h-8" />}
            title="Multi-Channel"
            description="Email, WhatsApp, and Web support"
            color="from-blue-500 to-purple-600"
            delay={0}
          />
          <FeatureCard
            icon={<Clock className="w-8 h-8" />}
            title="24/7 Available"
            description="AI-powered instant responses"
            color="from-green-500 to-emerald-600"
            delay={0.1}
          />
          <FeatureCard
            icon={<Shield className="w-8 h-8" />}
            title="Secure & Private"
            description="Your data is protected"
            color="from-orange-500 to-red-600"
            delay={0.2}
          />
        </div>

        {/* Main Content */}
        <div className="flex flex-col lg:flex-row gap-8 items-start justify-center">
          {/* Support Form */}
          <SupportForm onTicketCreated={handleTicketCreated} />

          {/* Status Card */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3, duration: 0.5 }}
          >
            <div className="w-full max-w-md">
              <div className="card-3d p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-3 bg-gradient-to-r from-[#28A745] to-[#1e7e34] rounded-lg">
                  <Ticket className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-gray-900">Check Status</h2>
                  <p className="text-sm text-gray-500">Track your support request</p>
                </div>
              </div>

              <p className="text-gray-600 mb-6">
                Already submitted a request? Check its status and view the conversation history.
              </p>

              <button
                onClick={openModal}
                className="btn-success w-full py-3 text-white font-semibold rounded-lg flex items-center justify-center gap-2 mb-3"
              >
                <Ticket className="w-5 h-5" />
                Check Ticket Status
              </button>

              <button
                onClick={openAnalytics}
                className="w-full py-3 bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700 text-white font-semibold rounded-lg flex items-center justify-center gap-2 transition-all"
              >
                <BarChart3 className="w-5 h-5" />
                Analytics Dashboard
              </button>

              {lastTicketId && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                >
                  <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                    <p className="text-sm text-green-800">
                      <strong>Latest Ticket:</strong> {lastTicketId}
                    </p>
                    <button
                      onClick={openModal}
                      className="text-xs text-green-600 hover:text-green-800 mt-1 underline font-medium"
                    >
                      View status →
                    </button>
                  </div>
                </motion.div>
              )}

              {/* Info Box */}
              <motion.div
                whileHover={{ scale: 1.02 }}
              >
                <div className="mt-6 p-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg shadow-lg">
                  <h3 className="font-semibold text-white mb-2 flex items-center gap-2">
                    <motion.span
                      animate={{ rotate: [0, 10, -10, 0] }}
                      transition={{ duration: 2, repeat: Infinity }}
                    >
                      ⚡
                    </motion.span>
                    Fast Response
                  </h3>
                  <p className="text-sm text-white/90">
                    Our AI agent typically responds within <strong className="text-yellow-300">3 seconds</strong>.
                    For escalated tickets, a human agent will respond within 24 hours.
                  </p>
                </div>
              </motion.div>

              {/* Quick Stats */}
              <div className="mt-4 grid grid-cols-2 gap-3">
                <motion.div 
                  whileHover={{ scale: 1.05 }}
                >
                  <div className="p-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg shadow-md">
                    <motion.p
                      animate={{ scale: [1, 1.1, 1] }}
                      transition={{ duration: 2, repeat: Infinity }}
                    >
                      <span className="text-2xl font-bold text-white">
                        98%
                      </span>
                    </motion.p>
                    <p className="text-xs text-white/80">Satisfaction</p>
                  </div>
                </motion.div>
                <motion.div 
                  whileHover={{ scale: 1.05 }}
                >
                  <div className="p-3 bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg shadow-md">
                    <motion.p 
                      animate={{ scale: [1, 1.1, 1] }}
                      transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
                    >
                      <span className="text-2xl font-bold text-white">
                        2.3s
                      </span>
                    </motion.p>
                    <p className="text-xs text-white/80">Avg Response</p>
                  </div>
                </motion.div>
              </div>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Footer */}
        <motion.footer
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5, duration: 0.5 }}
        >
          <div className="mt-16 text-center">
            <p className="text-sm text-white/90 dark:text-gray-200">
              Powered by AI • Multi-Channel Support • Customer Success FTE
            </p>
            <p className="text-xs mt-2 text-white/80 dark:text-gray-300">
              Built with ❤️ for Hackathon 5
            </p>
          </div>
        </motion.footer>
      </div>

      {/* Ticket Status Modal */}
      <TicketStatusModal 
        isOpen={isModalOpen} 
        onClose={closeModal} 
        onSuccess={(msg) => success(msg, 4000)}
        onError={(msg) => error(msg, 5000)}
      />

      {/* Analytics Dashboard Modal */}
      {isAnalyticsOpen && (
        <div
          className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm overflow-y-auto"
          onClick={closeAnalytics}
        >
          <div 
            onClick={(e) => e.stopPropagation()} 
            className="bg-white rounded-2xl shadow-2xl w-full max-w-5xl my-8 max-h-[90vh] overflow-y-auto"
          >
            <div className="flex items-center justify-between p-6 border-b border-gray-200 sticky top-0 bg-white z-10 rounded-t-2xl">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-gradient-to-r from-purple-500 to-pink-600 rounded-lg">
                  <BarChart3 className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-gray-900">Analytics Dashboard</h2>
                  <p className="text-sm text-gray-500">Sentiment analysis and performance metrics</p>
                </div>
              </div>
              <button
                onClick={closeAnalytics}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                aria-label="Close"
              >
                <svg className="w-6 h-6 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="p-6">
              <AnalyticsDashboard />
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <QuickActions />
    </div>
  );
}

// Feature Card Component
function FeatureCard({
  icon,
  title,
  description,
  color,
  delay,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
  color: string;
  delay: number;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      whileHover={{ scale: 1.05, y: -5 }}
    >
      <div className="card-3d p-6 text-center">
        <motion.div
          whileHover={{ rotate: 360 }}
          transition={{ duration: 0.6 }}
        >
          <div className={`inline-flex p-3 rounded-full bg-gradient-to-r ${color} text-white mb-4`}>
            {icon}
          </div>
        </motion.div>
        <h3 className="text-lg font-bold text-gray-900 mb-2">{title}</h3>
        <p className="text-gray-600">{description}</p>
      </div>
    </motion.div>
  );
}
