'use client';

/**
 * Quick Actions Button
 * A floating chat bubble that shows helpful keyboard shortcuts and tips
 */
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageCircle, X, Keyboard, Zap, Lightbulb, Clock } from 'lucide-react';

export default function QuickActions() {
  const [isOpen, setIsOpen] = useState(false);

  const shortcuts = [
    { icon: <Keyboard className="w-5 h-5" />, label: 'Shortcuts', tip: 'Press Ctrl+Enter to submit form' },
    { icon: <Zap className="w-5 h-5" />, label: 'Fast Response', tip: 'AI responds within 3 seconds' },
    { icon: <Lightbulb className="w-5 h-5" />, label: 'Pro Tip', tip: 'Be specific for better AI responses' },
    { icon: <Clock className="w-5 h-5" />, label: 'Available', tip: '24/7 support, even on holidays' },
  ];

  const quickTemplates = [
    { emoji: '🔐', label: 'Login Issue', message: "I'm having trouble logging into my account. Can you help reset my password?" },
    { emoji: '💳', label: 'Billing Question', message: 'I have a question about my recent invoice. Can you explain the charges?' },
    { emoji: '🐛', label: 'Report a Bug', message: 'I found a bug in the system. Let me describe what happened...' },
    { emoji: '⭐', label: 'Feedback', message: 'I wanted to share some feedback about your service...' },
  ];

  return (
    <>
      {/* Floating Chat Bubble Button */}
      <div
        className="fixed bottom-6 right-6 z-[150]"
      >
        <motion.button
          onClick={() => setIsOpen(!isOpen)}
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.5, type: 'spring', stiffness: 200 }}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          className="relative w-14 h-14 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 shadow-lg flex items-center justify-center text-white"
        >
          <AnimatePresence mode="wait">
            {isOpen ? (
              <motion.div
                key="close"
                initial={{ rotate: -90, opacity: 0 }}
                animate={{ rotate: 0, opacity: 1 }}
                exit={{ rotate: 90, opacity: 0 }}
              >
                <X className="w-7 h-7" />
              </motion.div>
            ) : (
              <motion.div
                key="open"
                initial={{ rotate: 90, opacity: 0 }}
                animate={{ rotate: 0, opacity: 1 }}
                exit={{ rotate: -90, opacity: 0 }}
              >
                <MessageCircle className="w-7 h-7" />
              </motion.div>
            )}
          </AnimatePresence>
          
          {/* Glow Effect */}
          <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full blur-lg opacity-50 animate-pulse" />
        </motion.button>
      </div>

      {/* Quick Actions Panel */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed bottom-24 right-6 z-[150] w-72"
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.9 }}
          >
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl overflow-hidden">
              {/* Header */}
              <div className="bg-gradient-to-r from-blue-500 to-purple-600 px-4 py-3">
                <h3 className="text-white font-bold text-lg flex items-center gap-2">
                  <MessageCircle className="w-5 h-5" />
                  Quick Actions
                </h3>
                <p className="text-white/80 text-xs mt-1">Helpful tips & shortcuts</p>
              </div>

              {/* Content */}
              <div className="p-4 space-y-4 max-h-96 overflow-y-auto custom-scrollbar">
                {/* Shortcuts Section */}
                <div>
                  <h4 className="text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase mb-2">
                    💡 Tips & Shortcuts
                  </h4>
                  <div className="space-y-2">
                    {shortcuts.map((item, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.05 }}
                        whileHover={{ scale: 1.02, x: 5 }}
                        className="flex items-start gap-3 p-3 rounded-lg bg-gray-50 dark:bg-gray-700 hover:bg-blue-50 dark:hover:bg-gray-600 transition-all cursor-pointer"
                      >
                        <div className="text-blue-500 dark:text-blue-400">
                          {item.icon}
                        </div>
                        <div>
                          <p className="font-semibold text-gray-900 dark:text-white text-sm">
                            {item.label}
                          </p>
                          <p className="text-xs text-gray-600 dark:text-gray-300 mt-0.5">
                            {item.tip}
                          </p>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </div>

                {/* Quick Templates Section */}
                <div>
                  <h4 className="text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase mb-2">
                    ⚡ Quick Templates
                  </h4>
                  <div className="space-y-2">
                    {quickTemplates.map((template, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.2 + index * 0.05 }}
                        whileHover={{ scale: 1.02, x: 5 }}
                        className="flex items-center gap-3 p-3 rounded-lg bg-green-50 dark:bg-gray-700 hover:bg-green-100 dark:hover:bg-gray-600 transition-all cursor-pointer"
                        onClick={() => {
                          // Copy to clipboard
                          navigator.clipboard.writeText(template.message);
                        }}
                      >
                        <span className="text-xl">{template.emoji}</span>
                        <div>
                          <p className="font-semibold text-gray-900 dark:text-white text-sm">
                            {template.label}
                          </p>
                          <p className="text-xs text-gray-600 dark:text-gray-400 mt-0.5 truncate">
                            {template.message.substring(0, 50)}...
                          </p>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-2 text-center">
                    Click to copy template
                  </p>
                </div>
              </div>

              {/* Footer */}
              <div className="px-4 py-3 bg-gray-50 dark:bg-gray-700 border-t border-gray-200 dark:border-gray-600">
                <p className="text-xs text-center text-gray-500 dark:text-gray-400">
                  💡 Need help? Just ask!
                </p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
