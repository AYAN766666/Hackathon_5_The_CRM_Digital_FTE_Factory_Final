'use client';

/**
 * Typing Indicator Component
 * Shows animated dots when AI is typing
 */
import React from 'react';
import { motion } from 'framer-motion';

export default function TypingIndicator() {
  return (
    <div className="flex items-center gap-2 p-4 bg-gray-100 rounded-2xl rounded-tl-none max-w-fit">
      <motion.span
        animate={{ y: [0, -8, 0] }}
        transition={{ duration: 0.6, repeat: Infinity, delay: 0 }}
        style={{ width: '8px', height: '8px', backgroundColor: '#9ca3af', borderRadius: '50%' }}
      />
      <motion.span
        animate={{ y: [0, -8, 0] }}
        transition={{ duration: 0.6, repeat: Infinity, delay: 0.2 }}
        style={{ width: '8px', height: '8px', backgroundColor: '#9ca3af', borderRadius: '50%' }}
      />
      <motion.span
        animate={{ y: [0, -8, 0] }}
        transition={{ duration: 0.6, repeat: Infinity, delay: 0.4 }}
        style={{ width: '8px', height: '8px', backgroundColor: '#9ca3af', borderRadius: '50%' }}
      />
    </div>
  );
}
