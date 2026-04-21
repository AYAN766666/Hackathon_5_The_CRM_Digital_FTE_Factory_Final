'use client';

/**
 * Global Error Page
 * Beautiful error handling with soft colors (NO RED!)
 */
import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { RefreshCw, Home, AlertCircle, Zap } from 'lucide-react';
import Link from 'next/link';

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function Error({ error, reset }: ErrorProps) {
  const [isMounted, setIsMounted] = useState(false);
  const [particles, setParticles] = useState<Array<{ x: number; y: number; type: number; duration: number; delay: number }>>([]);

  useEffect(() => {
    console.error('Error caught by error boundary:', error);
    setIsMounted(true);
    // Generate random particles on client side only
    setParticles(
      Array.from({ length: 15 }, (_, i) => ({
        x: Math.random() * (typeof window !== 'undefined' ? window.innerWidth : 1000),
        y: Math.random() * (typeof window !== 'undefined' ? window.innerHeight : 800),
        type: i % 3,
        duration: 5 + Math.random() * 3,
        delay: Math.random() * 2,
      }))
    );
  }, [error]);

  if (!isMounted) {
    return null;
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-800 via-blue-900 to-purple-900">
        <motion.div
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
          className="absolute top-0 left-0 w-96 h-96 bg-orange-500/20 rounded-full blur-3xl"
        />
        <motion.div
          animate={{
            scale: [1, 1.3, 1],
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: 'easeInOut',
            delay: 1,
          }}
          className="absolute bottom-0 right-0 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl"
        />
      </div>

      {/* Floating Geometric Shapes */}
      {particles.map((particle, i) => (
        <motion.div
          key={i}
          className="absolute"
          initial={{
            x: particle.x,
            y: particle.y,
          }}
          animate={{
            y: [null, particle.y - 150],
            rotate: [0, 360],
            opacity: [0, 0.5, 0],
          }}
          transition={{
            duration: particle.duration,
            repeat: Infinity,
            delay: particle.delay,
          }}
        >
          {particle.type === 0 ? (
            <div className="w-3 h-3 bg-orange-300/40 rotate-45" />
          ) : particle.type === 1 ? (
            <div className="w-4 h-4 bg-blue-300/40 rounded-full" />
          ) : (
            <div className="w-2 h-2 bg-purple-300/40" />
          )}
        </motion.div>
      ))}

      {/* Main Content */}
      <div className="relative z-10 text-center max-w-2xl">
        {/* Animated Error Icon */}
        <motion.div
          initial={{ opacity: 0, scale: 0.5, rotate: -180 }}
          animate={{ opacity: 1, scale: 1, rotate: 0 }}
          transition={{ duration: 0.8, type: 'spring' }}
          className="mb-8"
        >
          <motion.div
            animate={{
              rotate: [0, 10, -10, 0],
              scale: [1, 1.1, 1],
            }}
            transition={{
              duration: 3,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
            className="inline-block"
          >
            <div className="relative">
              {/* Glowing Orb */}
              <div className="absolute inset-0 bg-orange-400/50 rounded-full blur-2xl scale-150" />
              <div className="relative bg-gradient-to-br from-orange-400 to-amber-500 p-8 rounded-full shadow-2xl">
                <AlertCircle className="w-20 h-20 text-white" />
              </div>
              
              {/* Orbiting Ring */}
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 8, repeat: Infinity, ease: 'linear' }}
                className="absolute inset-0 border-2 border-dashed border-orange-300/30 rounded-full scale-150"
              />
            </div>
          </motion.div>
        </motion.div>

        {/* Error Title */}
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="text-4xl md:text-5xl font-bold text-white mb-4"
        >
          Oops! Something went wrong
        </motion.h1>

        {/* Error Message */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.5 }}
          className="text-xl text-gray-300 mb-8"
        >
          Don't worry, our team has been notified and we're on it!
        </motion.p>

        {/* Error Details Card */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ delay: 0.5 }}
              className="mb-8"
            >
              <div className="p-6 bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 max-w-md mx-auto">
                <div className="flex items-center gap-3 mb-3">
                  <Zap className="w-5 h-5 text-yellow-300" />
                  <h3 className="text-lg font-semibold text-white">Error Details</h3>
                </div>
                <p className="text-gray-300 text-sm font-mono bg-black/20 p-3 rounded-lg overflow-x-auto">
                  {error.message || 'An unexpected error occurred'}
                </p>
                {error.digest && (
                  <p className="text-gray-400 text-xs mt-2">
                    Reference ID: {error.digest}
                  </p>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.5 }}
          className="flex flex-col sm:flex-row gap-4 justify-center items-center"
        >
          <motion.button
            whileHover={{ scale: 1.05, boxShadow: '0 10px 40px rgba(255,255,255,0.2)' }}
            whileTap={{ scale: 0.95 }}
            onClick={reset}
            className="px-8 py-4 bg-gradient-to-r from-orange-400 to-amber-500 text-white font-bold rounded-full flex items-center gap-2 shadow-2xl transition-all"
          >
            <RefreshCw className="w-5 h-5" />
            Try Again
          </motion.button>
          
          <Link href="/">
            <motion.button
              whileHover={{ scale: 1.05, backgroundColor: 'rgba(255,255,255,0.2)' }}
              whileTap={{ scale: 0.95 }}
              className="px-8 py-4 bg-white/10 backdrop-blur-sm text-white font-semibold rounded-full flex items-center gap-2 border-2 border-white/30 hover:border-white/50 transition-all"
            >
              <Home className="w-5 h-5" />
              Back to Home
            </motion.button>
          </Link>
        </motion.div>

        {/* Help Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7, duration: 0.5 }}
          className="mt-12"
        >
          <div className="p-6 bg-gradient-to-r from-blue-500/20 to-purple-500/20 backdrop-blur-md rounded-2xl border border-white/10 max-w-lg mx-auto">
            <motion.div
              animate={{ rotate: [0, 5, -5, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="text-3xl mb-3"
            >
              💡
            </motion.div>
            <h3 className="text-lg font-semibold text-white mb-2">Need immediate help?</h3>
            <p className="text-gray-300 text-sm mb-4">
              Our support team is available 24/7 to assist you.
            </p>
            <Link href="/">
              <motion.span
                whileHover={{ scale: 1.05 }}
                className="inline-block px-6 py-2 bg-white/20 backdrop-blur-sm text-white rounded-full text-sm font-medium cursor-pointer hover:bg-white/30 transition-all"
              >
                Contact Support →
              </motion.span>
            </Link>
          </div>
        </motion.div>

        {/* Status Indicators */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="mt-8 flex justify-center gap-6"
        >
          <div className="flex items-center gap-2">
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="w-3 h-3 bg-green-400 rounded-full"
            />
            <span className="text-gray-400 text-sm">System Status: Operational</span>
          </div>
          <div className="flex items-center gap-2">
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
              className="w-3 h-3 bg-blue-400 rounded-full"
            />
            <span className="text-gray-400 text-sm">Support: Available</span>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
