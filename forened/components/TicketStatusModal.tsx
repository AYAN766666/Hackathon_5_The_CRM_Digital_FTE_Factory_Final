'use client';

/**
 * Ticket Status Modal Component
 * Displays conversation history with animated message bubbles and sentiment analysis
 */
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Ticket, Clock, MessageSquare, User, Bot, Trash2, CheckCircle, Download, Zap, AlertTriangle, Shield } from 'lucide-react';
import { getTicketStatus, type TicketStatusResponse, type Message, deleteTicket, APIError } from '@/lib/api';
import { getSentimentInfo } from '@/lib/sentiment';
import TypingIndicator from '@/components/TypingIndicator';

interface TicketStatusModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: (message: string) => void;
  onError?: (message: string) => void;
}

export default function TicketStatusModal({ isOpen, onClose, onSuccess, onError }: TicketStatusModalProps) {
  const [ticketId, setTicketId] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [ticketData, setTicketData] = useState<TicketStatusResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [deleteResult, setDeleteResult] = useState<{ success: boolean; message: string } | null>(null);

  // Handle ticket lookup
  const handleLookup = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!ticketId.trim()) {
      setError('Please enter a ticket ID');
      return;
    }

    setIsLoading(true);
    setError(null);
    setDeleteResult(null);

    try {
      const response = await getTicketStatus(ticketId.trim());
      console.log('Ticket Data Received:', response);
      console.log('Messages:', response.messages);
      setTicketData(response);
      setError(null);
    } catch (err: any) {
      // Extract user-friendly error message
      let errorMessage = 'Ticket not found';
      
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
      setTicketData(null);
      if (onError) onError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle ticket deletion
  const handleDelete = async () => {
    if (!ticketData) return;

    if (!confirm(`Are you sure you want to delete ticket ${ticketData.ticket_id}? This action cannot be undone.`)) {
      return;
    }

    setIsDeleting(true);
    setDeleteResult(null);

    try {
      const response = await deleteTicket(ticketData.ticket_id);
      setDeleteResult({ success: true, message: response.message });

      // Show success toast
      if (onSuccess) onSuccess('Ticket deleted successfully!');

      // Clear ticket data after successful deletion
      setTimeout(() => {
        setTicketData(null);
        setTicketId('');
        setDeleteResult(null);
        onClose();
      }, 1500);
    } catch (err: any) {
      // Extract user-friendly error message
      let errorMessage = 'Failed to delete ticket';
      
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
      
      setDeleteResult({ success: false, message: errorMessage });
      if (onError) onError(errorMessage);
    } finally {
      setIsDeleting(false);
    }
  };

  // Handle export conversation
  const handleExport = () => {
    if (!ticketData) return;

    // Create text content
    let exportContent = `TICKET: ${ticketData.ticket_id}\n`;
    exportContent += `Status: ${ticketData.status.toUpperCase()}\n`;
    exportContent += `Channel: ${ticketData.channel.toUpperCase()}\n`;
    exportContent += `Created: ${new Date(ticketData.created_at).toLocaleString()}\n`;
    exportContent += `${'='.repeat(50)}\n\n`;
    exportContent += `CONVERSATION HISTORY:\n\n`;

    ticketData.messages.slice().reverse().forEach((msg, index) => {
      const sender = msg.sender === 'customer' ? 'Customer' : 'Agent';
      const time = new Date(msg.timestamp).toLocaleString();
      exportContent += `[${index + 1}] ${sender} - ${time}\n`;
      exportContent += `${msg.content}\n\n`;
      if (msg.sentiment_score !== undefined) {
        const sentiment = getSentimentInfo(msg.sentiment_score);
        exportContent += `Sentiment: ${sentiment.label} ${sentiment.emoji}\n\n`;
      }
      exportContent += `${'-'.repeat(40)}\n`;
    });

    exportContent += `\n${'='.repeat(50)}\n`;
    exportContent += `Exported on: ${new Date().toLocaleString()}\n`;

    // Download as text file
    const blob = new Blob([exportContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ticket-${ticketData.ticket_id}-export.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Format timestamp
  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // Get status color
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'closed':
        return 'bg-gray-100 text-gray-800 border-gray-300';
      case 'escalated':
        return 'bg-red-100 text-red-800 border-red-300';
      default:
        return 'bg-blue-100 text-blue-800 border-blue-300';
    }
  };

  // Get sender icon
  const getSenderIcon = (sender: string) => {
    if (sender === 'customer') {
      return <User className="w-4 h-4" />;
    }
    return <Bot className="w-4 h-4" />;
  };

  // Get priority badge
  const getPriorityBadge = (priority: string | null, urgencyKeywords: string[] | null) => {
    if (!priority && !urgencyKeywords) return null;

    const priorityConfig: any = {
      critical: { color: 'bg-red-600', text: 'text-red-600', icon: <AlertTriangle className="w-3 h-3" />, label: 'CRITICAL' },
      high: { color: 'bg-orange-500', text: 'text-orange-500', icon: <Zap className="w-3 h-3" />, label: 'HIGH' },
      normal: { color: 'bg-blue-500', text: 'text-blue-500', icon: <Shield className="w-3 h-3" />, label: 'NORMAL' },
      low: { color: 'bg-gray-500', text: 'text-gray-500', icon: null, label: 'LOW' }
    };

    const config = priorityConfig[priority || 'normal'];

    return (
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        className={`inline-flex items-center gap-1 px-2 py-0.5 ${config.color} text-white text-xs font-bold rounded-full`}
      >
        {config.icon}
        <span>{config.label}</span>
        {urgencyKeywords && urgencyKeywords.length > 0 && (
          <span className="ml-1 text-[10px] opacity-80">
            ({urgencyKeywords.slice(0, 2).join(', ')})
          </span>
        )}
      </motion.div>
    );
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Overlay */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div onClick={onClose} className="modal-overlay fixed inset-0 z-50 flex items-center justify-center p-4">
            {/* Modal Content */}
            <motion.div
              initial={{ opacity: 0, y: -20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -20, scale: 0.95 }}
            >
              <div onClick={(e) => e.stopPropagation()} className="modal-content w-full max-w-2xl max-h-[80vh] overflow-hidden">
              {/* Header */}
              <div className="flex items-center justify-between p-6 border-b border-gray-200">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-gradient-to-r from-[#4F8DF7] to-[#1A5CC8] rounded-lg">
                    <Ticket className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h2 className="text-xl font-bold text-gray-900">Ticket Status</h2>
                    <p className="text-sm text-gray-500">Check your support request status</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={onClose}
                    className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                    aria-label="Close"
                  >
                    <X className="w-6 h-6 text-gray-500" />
                  </button>
                </div>
              </div>

              {/* Body */}
              <div className="p-6 overflow-y-auto custom-scrollbar" style={{ maxHeight: 'calc(80vh - 140px)' }}>
                {/* Search Form */}
                <form onSubmit={handleLookup} className="mb-6">
                  <label htmlFor="ticketId" className="block text-sm font-medium text-gray-700 mb-2">
                    Enter Ticket ID
                  </label>
                  <div className="flex gap-3">
                    <input
                      type="text"
                      id="ticketId"
                      value={ticketId}
                      onChange={(e) => setTicketId(e.target.value)}
                      className="input-modern flex-1 px-4 py-3 rounded-lg border border-gray-200 focus:border-[#4F8DF7]"
                      placeholder="e.g., ABC12345"
                      disabled={isLoading}
                    />
                    <button
                      type="submit"
                      disabled={isLoading}
                      className="btn-gradient px-6 py-3 text-white font-semibold rounded-lg disabled:opacity-50"
                    >
                      {isLoading ? (
                        <span className="flex items-center gap-2">
                          <span className="spinner w-4 h-4 border-2" />
                          Loading...
                        </span>
                      ) : (
                        'Check Status'
                      )}
                    </button>
                  </div>
                  {error && (
                    <motion.div
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                    >
                      <p className="mt-2 text-sm text-gray-700 bg-gray-100 px-3 py-2 rounded-lg inline-flex items-center gap-1">
                        <AlertTriangle className="w-4 h-4 text-orange-500" />
                        {error}
                      </p>
                    </motion.div>
                  )}
                </form>

                {/* Ticket Information */}
                {ticketData && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                  >
                    {/* Delete Result Message */}
                    <AnimatePresence>
                      {deleteResult && (
                        <motion.div
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: 'auto' }}
                          exit={{ opacity: 0, height: 0 }}
                        >
                          <div className={`mb-6 p-4 rounded-lg flex items-center gap-3 ${
                            deleteResult.success
                              ? 'bg-green-50 border border-green-200'
                              : 'bg-gray-100 border border-gray-200'
                          }`}>
                            {deleteResult.success ? (
                              <CheckCircle className="w-6 h-6 text-[#28A745] flex-shrink-0" />
                            ) : (
                              <AlertTriangle className="w-6 h-6 text-orange-500 flex-shrink-0" />
                            )}
                            <div className="flex-1">
                              <p
                                className={`font-semibold ${
                                  deleteResult.success ? 'text-green-800' : 'text-gray-800'
                                }`}
                              >
                                {deleteResult.message}
                              </p>
                            </div>
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>

                    <div className="space-y-4">
                      {/* Ticket Meta */}
                      <div className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
                      <div className="flex-1">
                        <p className="text-sm text-gray-600">Ticket ID</p>
                        <p className="text-lg font-bold text-gray-900">{ticketData.ticket_id}</p>
                      </div>
                      <div className="flex-1">
                        <p className="text-sm text-gray-600">Status</p>
                        <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold border ${getStatusColor(ticketData.status)}`}>
                          {ticketData.status.toUpperCase()}
                        </span>
                      </div>
                      <div className="flex-1">
                        <p className="text-sm text-gray-600">Channel</p>
                        <p className="text-lg font-semibold text-gray-900 capitalize">{ticketData.channel}</p>
                      </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="mt-4 flex justify-end gap-2">
                      <button
                        onClick={handleExport}
                        disabled={!ticketData}
                        className="flex items-center gap-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        <Download className="w-4 h-4" />
                        Export
                      </button>
                      <button
                        onClick={handleDelete}
                        disabled={isDeleting || !ticketData}
                        className="flex items-center gap-2 px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {isDeleting ? (
                          <>
                            <span className="spinner w-4 h-4 border-2" />
                            Deleting...
                          </>
                        ) : (
                          <>
                            <Trash2 className="w-4 h-4" />
                            Delete
                          </>
                        )}
                      </button>
                    </div>

                    {/* Messages */}
                    <div>
                      <div className="flex items-center gap-2 mb-4">
                        <MessageSquare className="w-5 h-5 text-[#4F8DF7]" />
                        <h3 className="text-lg font-semibold text-gray-900">Conversation History</h3>
                      </div>

                      <div className="space-y-3">
                        {ticketData.messages.slice().reverse().map((message, index) => {
                          const sentiment = getSentimentInfo(message.sentiment_score);
                          console.log(`Rendering message ${index}:`, message.sender, message.content.substring(0, 50));
                          return (
                          <motion.div
                            key={index}
                            initial={{ opacity: 0, x: message.sender === 'customer' ? -20 : 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: index * 0.1 }}
                          >
                            <div className={`flex gap-3 ${
                              message.sender === 'customer' ? 'flex-row' : 'flex-row-reverse'
                            }`}>
                            {/* Avatar */}
                            <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
                              message.sender === 'customer'
                                ? 'bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white'
                                : 'bg-gradient-to-r from-[#4F8DF7] to-[#1A5CC8] text-white'
                            }`}>
                              {getSenderIcon(message.sender)}
                            </div>

                            {/* Message Bubble */}
                            <div className={`flex-1 max-w-[75%]`}>
                              <div
                                className={`message-${message.sender} p-4 shadow-md`}
                              >
                                <p className="text-sm leading-relaxed">{message.content}</p>
                              </div>

                              {/* Message Meta */}
                              <div className={`flex items-center gap-2 mt-1 ${
                                message.sender === 'customer' ? 'justify-start' : 'justify-end'
                              }`}>
                                <span className="text-xs text-gray-500 flex items-center gap-1">
                                  <Clock className="w-3 h-3" />
                                  {formatTimestamp(message.timestamp)}
                                </span>
                                {/* Priority Badge */}
                                {message.priority && (
                                  <motion.div
                                    initial={{ scale: 0 }}
                                    animate={{ scale: 1 }}
                                    transition={{ delay: index * 0.1 + 0.2 }}
                                  >
                                    {getPriorityBadge(message.priority, message.urgency_keywords || null)}
                                  </motion.div>
                                )}
                                {/* Sentiment Badge */}
                                {message.sentiment_score !== undefined && (
                                  <motion.span
                                    initial={{ scale: 0 }}
                                    animate={{ scale: 1 }}
                                    transition={{ delay: index * 0.1 + 0.2, type: 'spring' }}
                                  >
                                    <span className={`text-xs px-2 py-1 rounded-full flex items-center gap-1 ${sentiment.bgColor} ${sentiment.color}`}>
                                      <span>{sentiment.emoji}</span>
                                      <span>{sentiment.label}</span>
                                    </span>
                                  </motion.span>
                                )}
                              </div>
                            </div>
                            </div>
                          </motion.div>
                        );
                        })}
                      </div>
                    </div>
                  </div>
                </motion.div>
                )}

                {/* Empty State */}
                {!ticketData && !isLoading && !error && (
                  <div className="text-center py-12">
                    <Ticket className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                    <p className="text-gray-500">Enter your ticket ID to view status and conversation history</p>
                  </div>
                )}
                </div>
              </div>
            </motion.div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
