'use client';

/**
 * Toast Notification System
 * Beautiful animated toast notifications
 */
import React, { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, AlertCircle, Info, X } from 'lucide-react';

export type ToastType = 'success' | 'error' | 'info';

interface Toast {
  id: string;
  type: ToastType;
  message: string;
  duration?: number;
}

interface ToastContainerProps {
  toasts: Toast[];
  onRemove: (id: string) => void;
}

export function useToast() {
  const [toasts, setToasts] = React.useState<Toast[]>([]);

  const addToast = (type: ToastType, message: string, duration = 5000) => {
    const id = Math.random().toString(36).substr(2, 9);
    const newToast: Toast = { id, type, message, duration };
    setToasts((prev) => [...prev, newToast]);

    // Auto remove after duration
    setTimeout(() => {
      removeToast(id);
    }, duration);
  };

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  };

  const success = (message: string, duration?: number) => {
    addToast('success', message, duration);
  };

  const error = (message: string, duration?: number) => {
    addToast('error', message, duration);
  };

  const info = (message: string, duration?: number) => {
    addToast('info', message, duration);
  };

  return { toasts, removeToast, success, error, info };
}

export default function ToastContainer({ toasts, onRemove }: ToastContainerProps) {
  const getIcon = (type: ToastType) => {
    switch (type) {
      case 'success':
        return <CheckCircle className="w-5 h-5" />;
      case 'error':
        return <AlertCircle className="w-5 h-5" />;
      case 'info':
        return <Info className="w-5 h-5" />;
    }
  };

  const getColors = (type: ToastType) => {
    switch (type) {
      case 'success':
        return 'bg-white border-l-4 border-green-500 text-gray-800 shadow-xl';
      case 'error':
        return 'bg-white border-l-4 border-orange-400 text-gray-800 shadow-xl';
      case 'info':
        return 'bg-white border-l-4 border-blue-500 text-gray-800 shadow-xl';
    }
  };

  const getIconColor = (type: ToastType) => {
    switch (type) {
      case 'success':
        return 'text-green-500';
      case 'error':
        return 'text-orange-500';
      case 'info':
        return 'text-blue-500';
    }
  };

  return (
    <div className="fixed top-4 right-4 z-[200] space-y-3">
      <AnimatePresence>
        {toasts.map((toast) => (
          <motion.div
            key={toast.id}
            initial={{ opacity: 0, x: 100, scale: 0.9 }}
            animate={{ opacity: 1, x: 0, scale: 1 }}
            exit={{ opacity: 0, x: 100, scale: 0.9 }}
            transition={{ duration: 0.3 }}
          >
            <div className={`flex items-center gap-3 p-4 rounded-lg shadow-lg min-w-[300px] max-w-md ${getColors(
              toast.type
            )}`}>
              <div className={getIconColor(toast.type)}>{getIcon(toast.type)}</div>
              <p className="flex-1 text-sm font-medium">{toast.message}</p>
              <button
                onClick={() => onRemove(toast.id)}
                className="p-1 hover:bg-gray-100 rounded transition-colors"
              >
                <X className="w-4 h-4 text-gray-400" />
              </button>
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
