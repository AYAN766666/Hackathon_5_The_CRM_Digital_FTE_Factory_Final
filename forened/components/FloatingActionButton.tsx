'use client';

/**
 * Floating Plus Button
 * Simple animated floating plus icon with glow effect
 */
import React from 'react';
import { motion } from 'framer-motion';
import { Plus, Sparkles } from 'lucide-react';

export default function FloatingPlusButton() {
  return (
    <div className="fixed bottom-6 right-6 z-[150]">
      {/* Floating Plus Button */}
      <motion.div
        initial={{ scale: 0 }}
        animate={{ 
          scale: 1,
          y: [0, -10, 0]
        }}
        transition={{
          scale: { delay: 0.5, type: 'spring', stiffness: 200 },
          y: { duration: 3, repeat: Infinity, ease: 'easeInOut' }
        }}
        whileHover={{ scale: 1.2, rotate: 180 }}
      >
        <div className="relative">
          {/* Glow Effect */}
          <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full blur-xl opacity-50 animate-pulse" />
          
          {/* Main Button */}
          <div className="relative w-16 h-16 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 shadow-lg flex items-center justify-center">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
            >
              <Plus className="w-8 h-8 text-white" strokeWidth={3} />
            </motion.div>
          </div>

          {/* Sparkles Around */}
          <motion.div
            animate={{ 
              scale: [1, 1.5, 1],
              rotate: [0, 180, 360]
            }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <div className="absolute -top-2 -right-2">
              <Sparkles className="w-6 h-6 text-yellow-300" />
            </div>
          </motion.div>

          {/* Small Dots Orbiting */}
          {[0, 120, 240].map((rotation, i) => (
            <motion.div
              key={i}
              style={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                width: '8px',
                height: '8px',
                borderRadius: '50%',
                backgroundColor: 'white',
              }}
              animate={{
                rotate: 360,
              }}
              transition={{
                duration: 3 + i,
                repeat: Infinity,
                ease: 'linear',
                delay: i * 0.3
              }}
            >
              <div 
                style={{
                  width: '8px',
                  height: '8px',
                  borderRadius: '50%',
                  backgroundColor: 'white',
                  transform: `rotate(${rotation}deg) translateY(-40px) translateX(-50%)`
                }}
              />
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Floating Badge */}
      <motion.div
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 1 }}
      >
        <div className="absolute bottom-full right-0 mb-2 mr-4 bg-white rounded-lg shadow-lg px-3 py-2">
          <div className="text-center">
            <p className="text-xs font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-600">
              AI Powered
            </p>
            <p className="text-[10px] text-gray-500">24/7 Support</p>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
