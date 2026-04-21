'use client';

/**
 * Support Form Component
 * Animated UI with gradient buttons and 3D effects
 */
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, RotateCcw, Ticket, CheckCircle, AlertCircle, Loader2, Sparkles, Lightbulb, X } from 'lucide-react';
import { submitSupportRequest, type SupportSubmitData, APIError } from '@/lib/api';
import TypingIndicator from '@/components/TypingIndicator';

interface SupportFormProps {
  onTicketCreated?: (ticketId: string) => void;
}

type CategoryType = 'General' | 'Technical' | 'Billing' | 'Feedback' | 'Bug Report';

interface FormData {
  name: string;
  email: string;
  category: CategoryType;
  message: string;
}

interface FormErrors {
  name?: string;
  email?: string;
  category?: string;
  message?: string;
}

const CATEGORIES: CategoryType[] = [
  'General',
  'Technical',
  'Billing',
  'Feedback',
  'Bug Report'
];

export default function SupportForm({ onTicketCreated }: SupportFormProps) {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
    category: 'General',
    message: ''
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showTyping, setShowTyping] = useState(false);
  const [submitResult, setSubmitResult] = useState<{
    success: boolean;
    message: string;
    ticketId?: string;
  } | null>(null);
  const [processingStep, setProcessingStep] = useState('');

  const [showSuggestions, setShowSuggestions] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);

  // Smart message templates based on keywords
  const messageTemplates = [
    {
      keywords: ['login', 'password', 'signin', 'account'],
      emoji: '🔐',
      label: 'Login Issue Template',
      message: "Hello, I'm experiencing issues with logging into my account. I've tried resetting my password but haven't received any email. Could you please help me regain access to my account? My registered email is "
    },
    {
      keywords: ['payment', 'billing', 'invoice', 'charge', 'refund'],
      emoji: '💳',
      label: 'Billing Question Template',
      message: "I have a question regarding my recent invoice. I noticed some charges that I don't recognize. Could you please provide a breakdown of the following charges? Also, I'd like to know about your refund policy."
    },
    {
      keywords: ['bug', 'error', 'issue', 'problem', 'not working'],
      emoji: '🐛',
      label: 'Bug Report Template',
      message: "I've encountered a bug in your system. Here are the details:\n\n1. What I was trying to do:\n2. What actually happened:\n3. Expected behavior:\n4. Browser/Device I'm using:\n\nCould you please look into this issue?"
    },
    {
      keywords: ['feature', 'suggestion', 'improvement', 'idea'],
      emoji: '💡',
      label: 'Feature Request Template',
      message: "I have a suggestion for improving your service. It would be great if you could add a feature that allows users to [describe feature]. This would help because [explain benefit]. Thank you for considering this suggestion!"
    },
    {
      keywords: ['slow', 'performance', 'loading', 'speed'],
      emoji: '⚡',
      label: 'Performance Issue Template',
      message: "I'm experiencing performance issues with your application. The system is running very slow, especially when [describe action]. Pages take a long time to load. Could you please investigate this performance issue?"
    },
  ];

  // Get suggestions based on user input
  const getSuggestions = () => {
    const input = formData.message.toLowerCase();
    if (input.length < 10) return [];

    return messageTemplates.filter(template =>
      template.keywords.some(keyword => input.includes(keyword))
    );
  };

  const suggestions = getSuggestions();

  const applyTemplate = (template: any) => {
    setFormData(prev => ({
      ...prev,
      message: template.message + prev.message
    }));
    setSelectedTemplate(template.label);
    setShowSuggestions(false);
  };

  // Validate form
  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    // Name validation (2-50 characters)
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    } else if (formData.name.length < 2 || formData.name.length > 50) {
      newErrors.name = 'Name must be between 2 and 50 characters';
    }

    // Email validation
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    // Message validation (20-1000 characters)
    if (!formData.message.trim()) {
      newErrors.message = 'Message is required';
    } else if (formData.message.length < 20 || formData.message.length > 1000) {
      newErrors.message = 'Message must be between 20 and 1000 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle input change
  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));

    // Clear error when user starts typing
    if (errors[name as keyof FormErrors]) {
      setErrors(prev => ({ ...prev, [name]: undefined }));
    }
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    setSubmitResult(null);
    setProcessingStep('🔍 Analyzing your request...');
    setShowTyping(true);

    // Show typing indicator for a moment
    setTimeout(async () => {
      try {
        setProcessingStep('🤖 AI is generating a response...');
        const response = await submitSupportRequest(formData);

        setProcessingStep('✅ Ticket created successfully!');
        setSubmitResult({
          success: true,
          message: response.message,
          ticketId: response.ticket_id
        });

        // Notify parent component
        if (onTicketCreated) {
          onTicketCreated(response.ticket_id);
        }

        // Reset form
        setFormData({
          name: '',
          email: '',
          category: 'General',
          message: ''
        });

      } catch (error: any) {
        setProcessingStep('');
        // Extract user-friendly error message
        let errorMessage = 'Failed to submit request. Please try again.';
        
        if (error instanceof APIError) {
          errorMessage = error.message;
          if (error.hint) {
            errorMessage += ` ${error.hint}`;
          }
        } else if (error.userMessage) {
          errorMessage = error.userMessage;
        } else if (error.message) {
          errorMessage = error.message;
        }

        setSubmitResult({
          success: false,
          message: errorMessage
        });
      } finally {
        setIsSubmitting(false);
        setShowTyping(false);
        setTimeout(() => setProcessingStep(''), 5000);
      }
    }, 1000);
  };

  // Handle reset
  const handleReset = () => {
    setFormData({
      name: '',
      email: '',
      category: 'General',
      message: ''
    });
    setErrors({});
    setSubmitResult(null);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="w-full max-w-2xl">
        <div className="card-3d p-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <div className="mb-8 text-center">
            <div className="flex items-center justify-center gap-2 mb-2">
            <motion.div
              animate={{ rotate: [0, 10, -10, 0] }}
              transition={{ duration: 2, repeat: Infinity, repeatDelay: 3 }}
            >
              <Sparkles className="w-6 h-6 text-[#4F8DF7]" />
            </motion.div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-[#4F8DF7] to-[#1A5CC8] bg-clip-text text-transparent">
              Customer Support
            </h1>
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 1.5, repeat: Infinity }}
            >
              <Sparkles className="w-6 h-6 text-[#1A5CC8]" />
            </motion.div>
          </div>
            <p className="text-gray-600">
              We're here to help! Submit your request and we'll get back to you shortly.
            </p>
          </div>
        </motion.div>

        {/* Success/Error Message */}
        <AnimatePresence>
          {submitResult && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
            >
              <div className={`mb-6 p-4 rounded-lg flex items-center gap-3 ${
                submitResult.success
                  ? 'bg-green-50 border-2 border-green-200'
                  : 'bg-orange-50 border-2 border-orange-200'
              }`}>
                {submitResult.success ? (
                  <CheckCircle className="w-6 h-6 text-[#28A745] flex-shrink-0" />
                ) : (
                  <AlertCircle className="w-6 h-6 text-orange-600 flex-shrink-0" />
                )}
                <div className="flex-1">
                  <p
                    className={`font-semibold ${
                      submitResult.success ? 'text-green-800' : 'text-orange-800'
                    }`}
                  >
                    {submitResult.message}
                  </p>
                  {submitResult.ticketId && (
                    <p className="text-green-700 mt-1">
                      <strong>Ticket ID:</strong> {submitResult.ticketId}
                    </p>
                  )}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Typing Indicator */}
        <AnimatePresence>
          {showTyping && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
            >
              <div className="mb-6 p-4 bg-blue-50 border-2 border-blue-200 rounded-lg flex items-center gap-3">
                <TypingIndicator />
                <div className="flex-1">
                  <p className="text-sm text-blue-800 font-medium">AI is processing your request...</p>
                  {processingStep && (
                    <p className="text-xs text-blue-600 mt-1">{processingStep}</p>
                  )}
                </div>
                <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Name Field */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
          >
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
              Name <span className="text-orange-500">*</span>
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              className={`input-modern w-full px-4 py-3 rounded-lg border ${
                errors.name ? 'border-orange-300 input-error' : 'border-gray-200'
              } focus:border-[#4F8DF7] transition-colors`}
              placeholder="Your name"
              disabled={isSubmitting || showTyping}
            />
            {errors.name && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <p className="mt-1 text-sm text-orange-600 flex items-center gap-1">
                  <AlertCircle className="w-4 h-4" />
                  {errors.name}
                </p>
              </motion.div>
            )}
          </motion.div>

          {/* Email Field */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
          >
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
              Email <span className="text-orange-500">*</span>
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              className={`input-modern w-full px-4 py-3 rounded-lg border ${
                errors.email ? 'border-orange-300 input-error' : 'border-gray-200'
              } focus:border-[#4F8DF7] transition-colors`}
              placeholder="your@email.com"
              disabled={isSubmitting || showTyping}
            />
            {errors.email && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <p className="mt-1 text-sm text-orange-600 flex items-center gap-1">
                  <AlertCircle className="w-4 h-4" />
                  {errors.email}
                </p>
              </motion.div>
            )}
          </motion.div>

          {/* Category Field */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
          >
            <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
              Category <span className="text-red-500">*</span>
            </label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleInputChange}
              className="input-modern w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-[#4F8DF7] transition-colors bg-white"
              disabled={isSubmitting || showTyping}
            >
              {CATEGORIES.map(cat => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </motion.div>

          {/* Message Field */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
          >
            <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-2">
              Message <span className="text-orange-500">*</span>
            </label>
            <div className="relative">
              <textarea
                id="message"
                name="message"
                value={formData.message}
                onChange={handleInputChange}
                onFocus={() => suggestions.length > 0 && setShowSuggestions(true)}
                onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
                rows={5}
                className={`input-modern w-full px-4 py-3 rounded-lg border ${
                  errors.message ? 'border-orange-300 input-error' : 'border-gray-200'
                } focus:border-[#4F8DF7] transition-colors resize-none`}
                placeholder="Describe your issue in detail (minimum 20 characters)..."
                disabled={isSubmitting || showTyping}
              />

              {/* Smart Suggestion Badge */}
              {formData.message.length >= 10 && suggestions.length > 0 && !showSuggestions && (
                <motion.button
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  whileHover={{ scale: 1.05 }}
                  onClick={() => setShowSuggestions(true)}
                  className="absolute bottom-3 right-3 flex items-center gap-1 px-3 py-1.5 bg-gradient-to-r from-yellow-400 to-orange-500 text-white text-xs font-semibold rounded-full shadow-lg hover:shadow-xl transition-all"
                >
                  <Lightbulb className="w-3 h-3" />
                  Smart Suggestion
                </motion.button>
              )}
            </div>

            {/* Smart Suggestions Popup */}
            <AnimatePresence>
              {showSuggestions && suggestions.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="mt-2 p-3 bg-gradient-to-r from-yellow-50 to-orange-50 border-2 border-yellow-300 rounded-lg"
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <Lightbulb className="w-4 h-4 text-yellow-600" />
                      <p className="text-sm font-semibold text-yellow-800">
                        Smart Suggestions
                      </p>
                    </div>
                    <button
                      onClick={() => setShowSuggestions(false)}
                      className="text-yellow-600 hover:text-yellow-800"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                  <div className="space-y-2">
                    {suggestions.map((template, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                      >
                        <button
                          onClick={() => applyTemplate(template)}
                          className="w-full text-left p-2 bg-white rounded-lg hover:bg-yellow-100 transition-all flex items-start gap-2"
                        >
                          <span className="text-lg">{template.emoji}</span>
                          <div>
                            <p className="text-sm font-semibold text-gray-800">
                              {template.label}
                            </p>
                            <p className="text-xs text-gray-600 truncate">
                              {template.message.substring(0, 80)}...
                            </p>
                          </div>
                        </button>
                      </motion.div>
                    ))}
                  </div>
                  {selectedTemplate && (
                    <motion.p
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="mt-2 text-xs text-green-600 font-medium"
                    >
                      ✓ Applied: {selectedTemplate}
                    </motion.p>
                  )}
                </motion.div>
              )}
            </AnimatePresence>
            <div className="flex justify-between items-center mt-1">
              {errors.message ? (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <p className="text-sm text-orange-600 flex items-center gap-1">
                    <AlertCircle className="w-4 h-4" />
                    {errors.message}
                  </p>
                </motion.div>
              ) : (
                <span />
              )}
              <motion.span
                animate={{ scale: formData.message.length >= 20 ? [1, 1.1, 1] : 1 }}
                transition={{ duration: 0.3 }}
              >
                <span className={`text-sm ${formData.message.length >= 20 ? 'text-green-600' : 'text-gray-500'}`}>
                  {formData.message.length}/1000
                </span>
              </motion.span>
            </div>
          </motion.div>

          {/* Action Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
          >
            <div className="flex gap-4 pt-4">
              {/* Submit Button */}
              <button
              type="submit"
              disabled={isSubmitting || showTyping}
              className="btn-gradient flex-1 flex items-center justify-center gap-2 text-white font-semibold py-3 px-6 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  {processingStep || 'Processing...'}
                </>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  Submit Request
                </>
              )}
            </button>

            {/* Reset Button */}
            <button
              type="button"
              onClick={handleReset}
              disabled={isSubmitting || showTyping}
              className="btn-reset flex items-center justify-center gap-2 text-gray-700 font-semibold py-3 px-6 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <RotateCcw className="w-5 h-5" />
              Reset
            </button>
            </div>
          </motion.div>
        </form>
        </div>
      </div>
    </motion.div>
  );
}
