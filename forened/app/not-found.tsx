'use client';

/**
 * 404 Not Found Page
 * Beautiful 3D animated error page
 */
import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Home, ArrowLeft, HelpCircle } from 'lucide-react';
import Link from 'next/link';

export default function NotFound() {
  const [isMounted, setIsMounted] = useState(false);
  const [particles, setParticles] = useState<Array<{ x: number; y: number; duration: number; delay: number }>>([]);

  useEffect(() => {
    setIsMounted(true);
    // Generate random particles on client side only
    setParticles(
      Array.from({ length: 20 }, () => ({
        x: Math.random() * (typeof window !== 'undefined' ? window.innerWidth : 1000),
        y: Math.random() * (typeof window !== 'undefined' ? window.innerHeight : 800),
        duration: 3 + Math.random() * 2,
        delay: Math.random() * 2,
      }))
    );
  }, []);

  if (!isMounted) {
    return null;
  }
  return (
    <div className="min-h-screen flex items-center justify-center px-4 relative overflow-hidden">
      {/* Animated Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
        <motion.div
          animate={{
            scale: [1, 1.2, 1],
            rotate: [0, 180, 360],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: 'linear',
          }}
          className="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-br from-blue-400/20 to-transparent rounded-full blur-3xl"
        />
        <motion.div
          animate={{
            scale: [1, 1.3, 1],
            rotate: [360, 180, 0],
          }}
          transition={{
            duration: 25,
            repeat: Infinity,
            ease: 'linear',
          }}
          className="absolute -bottom-1/2 -right-1/2 w-full h-full bg-gradient-to-tl from-orange-400/20 to-transparent rounded-full blur-3xl"
        />
      </div>

      {/* Floating Particles */}
      {particles.map((particle, i) => (
        <motion.div
          key={i}
          className="absolute w-2 h-2 bg-white/30 rounded-full"
          initial={{
            x: particle.x,
            y: particle.y,
          }}
          animate={{
            y: [null, particle.y - 100],
            opacity: [0, 1, 0],
          }}
          transition={{
            duration: particle.duration,
            repeat: Infinity,
            delay: particle.delay,
          }}
        />
      ))}

      {/* Main Content */}
      <div className="relative z-10 text-center">
        {/* 3D Animated 404 Number */}
        <motion.div
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8 }}
          className="mb-8"
        >
          <div className="relative">
            <motion.h1
              animate={{
                y: [0, -20, 0],
                rotateY: [0, 180, 360],
              }}
              transition={{
                duration: 6,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
              className="text-[200px] md:text-[300px] font-bold text-white/90 leading-none"
              style={{
                textShadow: `
                  0 1px 0 #ccc,
                  0 2px 0 #c9c9c9,
                  0 3px 0 #bbb,
                  0 4px 0 #b9b9b9,
                  0 5px 0 #aaa,
                  0 6px 1px rgba(0,0,0,.1),
                  0 0 5px rgba(0,0,0,.1),
                  0 1px 3px rgba(0,0,0,.3),
                  0 3px 5px rgba(0,0,0,.2),
                  0 5px 10px rgba(0,0,0,.25),
                  0 10px 10px rgba(0,0,0,.2),
                  0 20px 20px rgba(0,0,0,.15)
                `,
              }}
            >
              404
            </motion.h1>
            
            {/* Orbiting Elements */}
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 10, repeat: Infinity, ease: 'linear' }}
              className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] pointer-events-none"
            >
              <div className="absolute top-0 left-1/2 w-4 h-4 bg-yellow-300 rounded-full shadow-lg shadow-yellow-300/50" />
              <div className="absolute bottom-0 left-1/2 w-3 h-3 bg-blue-300 rounded-full shadow-lg shadow-blue-300/50" />
              <div className="absolute left-0 top-1/2 w-2 h-2 bg-pink-300 rounded-full shadow-lg shadow-pink-300/50" />
              <div className="absolute right-0 top-1/2 w-3 h-3 bg-green-300 rounded-full shadow-lg shadow-green-300/50" />
            </motion.div>
          </div>
        </motion.div>

        {/* Error Message */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="mb-8"
        >
          <motion.div
            animate={{ rotate: [0, 10, -10, 0] }}
            transition={{ duration: 3, repeat: Infinity }}
            className="inline-block mb-4"
          >
            <HelpCircle className="w-16 h-16 text-white/90 mx-auto" />
          </motion.div>
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Oops! Page not found
          </h2>
          <p className="text-xl text-white/80 max-w-md mx-auto">
            The page you're looking for seems to have wandered off into the digital void.
          </p>
        </motion.div>

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.5 }}
          className="flex flex-col sm:flex-row gap-4 justify-center items-center"
        >
          <Link href="/">
            <motion.button
              whileHover={{ scale: 1.05, boxShadow: '0 10px 40px rgba(255,255,255,0.3)' }}
              whileTap={{ scale: 0.95 }}
              className="px-8 py-4 bg-white text-purple-600 font-bold rounded-full flex items-center gap-2 shadow-2xl transition-all"
            >
              <Home className="w-5 h-5" />
              Back to Home
            </motion.button>
          </Link>
          
          <motion.button
            whileHover={{ scale: 1.05, backgroundColor: 'rgba(255,255,255,0.2)' }}
            whileTap={{ scale: 0.95 }}
            onClick={() => window.history.back()}
            className="px-8 py-4 bg-white/10 backdrop-blur-sm text-white font-semibold rounded-full flex items-center gap-2 border-2 border-white/30 hover:border-white/50 transition-all"
          >
            <ArrowLeft className="w-5 h-5" />
            Go Back
          </motion.button>
        </motion.div>

        {/* Fun Fact Card */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.7, duration: 0.5 }}
          className="mt-12 max-w-md mx-auto"
        >
          <div className="p-6 bg-white/10 backdrop-blur-md rounded-2xl border border-white/20">
            <motion.div
              animate={{ rotate: [0, 5, -5, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="text-4xl mb-2"
            >
              🚀
            </motion.div>
            <p className="text-white/90 text-sm">
              <strong className="text-yellow-300">Fun Fact:</strong> The first 404 error was named after Room 404 at CERN, where the web was invented!
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
