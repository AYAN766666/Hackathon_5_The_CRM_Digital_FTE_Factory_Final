'use client';

/**
 * 3D Error Animation Component
 * Reusable component for showing errors with beautiful animations
 * NO RED COLORS - uses soft oranges, ambers, and warm tones
 */
import React from 'react';
import { motion } from 'framer-motion';
import { AlertCircle, AlertTriangle, Info, XCircle } from 'lucide-react';

interface ErrorAnimationProps {
  type?: 'error' | 'warning' | 'info' | 'validation';
  title?: string;
  message?: string;
  showIcon?: boolean;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export default function ErrorAnimation({
  type = 'error',
  title,
  message,
  showIcon = true,
  size = 'md',
  className = '',
}: ErrorAnimationProps) {
  // Configuration based on type - NO RED COLORS!
  const config = {
    error: {
      icon: AlertCircle,
      gradient: 'from-orange-400 to-amber-500',
      bgColor: 'bg-orange-50',
      borderColor: 'border-orange-200',
      textColor: 'text-orange-900',
      lightTextColor: 'text-orange-700',
      glowColor: 'shadow-orange-400/50',
    },
    warning: {
      icon: AlertTriangle,
      gradient: 'from-yellow-400 to-amber-500',
      bgColor: 'bg-yellow-50',
      borderColor: 'border-yellow-200',
      textColor: 'text-yellow-900',
      lightTextColor: 'text-yellow-700',
      glowColor: 'shadow-yellow-400/50',
    },
    info: {
      icon: Info,
      gradient: 'from-blue-400 to-cyan-500',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200',
      textColor: 'text-blue-900',
      lightTextColor: 'text-blue-700',
      glowColor: 'shadow-blue-400/50',
    },
    validation: {
      icon: XCircle,
      gradient: 'from-purple-400 to-pink-500',
      bgColor: 'bg-purple-50',
      borderColor: 'border-purple-200',
      textColor: 'text-purple-900',
      lightTextColor: 'text-purple-700',
      glowColor: 'shadow-purple-400/50',
    },
  };

  const currentConfig = config[type];
  const IconComponent = currentConfig.icon;

  const sizeClasses = {
    sm: {
      container: 'p-3',
      icon: 'w-8 h-8',
      iconContainer: 'p-2',
      title: 'text-sm',
      message: 'text-xs',
    },
    md: {
      container: 'p-5',
      icon: 'w-12 h-12',
      iconContainer: 'p-3',
      title: 'text-base',
      message: 'text-sm',
    },
    lg: {
      container: 'p-6',
      icon: 'w-16 h-16',
      iconContainer: 'p-4',
      title: 'text-lg',
      message: 'text-base',
    },
  };

  const sizes = sizeClasses[size];

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9, y: -10 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.9, y: -10 }}
      transition={{ duration: 0.3, type: 'spring' }}
      className={`${currentConfig.bgColor} ${currentConfig.borderColor} border rounded-2xl shadow-lg ${sizes.container} ${className}`}
    >
      <div className="flex items-start gap-4">
        {/* Animated Icon with 3D Effect */}
        {showIcon && (
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
            className={`relative flex-shrink-0`}
          >
            {/* Glow Effect */}
            <div className={`absolute inset-0 ${currentConfig.gradient} rounded-full blur-lg opacity-50 scale-125`} />
            
            {/* Icon Container */}
            <div className={`relative bg-gradient-to-br ${currentConfig.gradient} ${sizes.iconContainer} rounded-full shadow-xl`}>
              <IconComponent className={`${sizes.icon} text-white`} />
            </div>

            {/* Orbiting Ring */}
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 8, repeat: Infinity, ease: 'linear' }}
              className={`absolute inset-0 border-2 border-dashed ${currentConfig.borderColor} rounded-full scale-150`}
            />
          </motion.div>
        )}

        {/* Text Content */}
        <div className="flex-1 min-w-0">
          {title && (
            <motion.h3
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.1 }}
              className={`${sizes.title} font-semibold ${currentConfig.textColor} mb-1`}
            >
              {title}
            </motion.h3>
          )}
          
          {message && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
              className={`${sizes.message} ${currentConfig.lightTextColor} leading-relaxed`}
            >
              {message}
            </motion.p>
          )}
        </div>
      </div>

      {/* Decorative Particles */}
      <div className="relative mt-3 h-8 overflow-hidden">
        {[...Array(5)].map((_, i) => (
          <motion.div
            key={i}
            className={`absolute w-1 h-1 ${currentConfig.gradient.replace('from-', 'bg-').split(' ')[0]} rounded-full opacity-60`}
            initial={{
              x: Math.random() * 100 + '%',
              y: '100%',
            }}
            animate={{
              y: '-100%',
              opacity: [0, 1, 0],
            }}
            transition={{
              duration: 2 + Math.random() * 2,
              repeat: Infinity,
              delay: Math.random() * 2,
            }}
          />
        ))}
      </div>
    </motion.div>
  );
}

// Inline Error Component for Form Fields
export function InlineError({ message, show = true }: { message: string; show?: boolean }) {
  if (!show) return null;

  return (
    <motion.div
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: 'auto' }}
      exit={{ opacity: 0, height: 0 }}
      className="flex items-center gap-2 mt-2 px-3 py-2 bg-orange-50 border border-orange-200 rounded-lg"
    >
      <motion.div
        animate={{ rotate: [0, 10, -10, 0] }}
        transition={{ duration: 2, repeat: Infinity }}
      >
        <AlertCircle className="w-4 h-4 text-orange-500" />
      </motion.div>
      <p className="text-sm text-orange-700">{message}</p>
    </motion.div>
  );
}

// Toast Error Component
export function ToastError({ message, onClose }: { message: string; onClose: () => void }) {
  return (
    <motion.div
      initial={{ opacity: 0, x: 100, scale: 0.8 }}
      animate={{ opacity: 1, x: 0, scale: 1 }}
      exit={{ opacity: 0, x: 100, scale: 0.8 }}
      className="flex items-center gap-3 px-4 py-3 bg-gradient-to-r from-orange-400 to-amber-500 text-white rounded-lg shadow-xl"
    >
      <motion.div
        animate={{ rotate: [0, 10, -10, 0] }}
        transition={{ duration: 2, repeat: Infinity }}
      >
        <AlertCircle className="w-5 h-5" />
      </motion.div>
      <p className="flex-1 text-sm font-medium">{message}</p>
      <motion.button
        whileHover={{ scale: 1.2 }}
        whileTap={{ scale: 0.9 }}
        onClick={onClose}
        className="p-1 hover:bg-white/20 rounded transition-colors"
      >
        <XCircle className="w-5 h-5" />
      </motion.button>
    </motion.div>
  );
}
