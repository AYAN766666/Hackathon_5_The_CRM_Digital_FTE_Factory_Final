'use client';

/**
 * Live Statistics Dashboard
 * Real-time counters with smooth animations
 */
import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Ticket, CheckCircle, Clock, Users, Zap, TrendingUp } from 'lucide-react';

interface Stats {
  totalTickets: number;
  resolved: number;
  active: number;
  avgResponseTime: number;
  satisfaction: number;
}

export default function LiveStats() {
  const [stats, setStats] = useState<Stats>({
    totalTickets: 0,
    resolved: 0,
    active: 0,
    avgResponseTime: 0,
    satisfaction: 0,
  });

  useEffect(() => {
    // Simulate live updates (in production, fetch from API)
    const updateStats = () => {
      setStats({
        totalTickets: 1247,
        resolved: 1189,
        active: 58,
        avgResponseTime: 2.3,
        satisfaction: 98,
      });
    };

    updateStats();

    // Update every 5 seconds to simulate live data
    const interval = setInterval(updateStats, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
    >
      <div className="w-full max-w-6xl mx-auto mb-8">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <StatCard
          icon={<Ticket className="w-6 h-6" />}
          label="Total Tickets"
          value={stats.totalTickets}
          color="from-blue-500 to-blue-600"
          suffix=""
        />
        <StatCard
          icon={<CheckCircle className="w-6 h-6" />}
          label="Resolved"
          value={stats.resolved}
          color="from-green-500 to-green-600"
          suffix=""
        />
        <StatCard
          icon={<Clock className="w-6 h-6" />}
          label="Active"
          value={stats.active}
          color="from-orange-500 to-orange-600"
          suffix=""
        />
        <StatCard
          icon={<Zap className="w-6 h-6" />}
          label="Avg Response"
          value={stats.avgResponseTime}
          color="from-purple-500 to-purple-600"
          suffix="s"
          isDecimal
        />
        <StatCard
          icon={<TrendingUp className="w-6 h-6" />}
          label="Satisfaction"
          value={stats.satisfaction}
          color="from-pink-500 to-pink-600"
          suffix="%"
        />
        <StatCard
          icon={<Users className="w-6 h-6" />}
          label="Success Rate"
          value={95}
          color="from-teal-500 to-teal-600"
          suffix="%"
        />
        </div>

        {/* Live Indicator */}
        <div className="text-center mt-4">
        <motion.div
          animate={{ scale: [1, 1.05, 1] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/20 backdrop-blur-sm rounded-full">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
            </span>
            <span className="text-white text-sm font-medium">Live Updates</span>
          </div>
        </motion.div>
        </div>
      </div>
    </motion.div>
  );
}

function StatCard({
  icon,
  label,
  value,
  color,
  suffix,
  isDecimal = false,
}: {
  icon: React.ReactNode;
  label: string;
  value: number;
  color: string;
  suffix: string;
  isDecimal?: boolean;
}) {
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    // Animate counter
    const duration = 1000;
    const steps = 20;
    const increment = value / steps;
    let current = 0;

    const timer = setInterval(() => {
      current += increment;
      if (current >= value) {
        setDisplayValue(value);
        clearInterval(timer);
      } else {
        setDisplayValue(current);
      }
    }, duration / steps);

    return () => clearInterval(timer);
  }, [value]);

  return (
    <motion.div
      whileHover={{ scale: 1.05, y: -5 }}
    >
      <div className="card-3d p-4 text-center">
        <div className={`inline-flex p-2 rounded-lg bg-gradient-to-r ${color} text-white mb-2`}>
          {icon}
        </div>
        <div className="text-2xl font-bold text-gray-900">
          {isDecimal ? displayValue.toFixed(1) : Math.floor(displayValue)}
          {suffix}
        </div>
        <div className="text-xs text-gray-600 mt-1">{label}</div>
      </div>
    </motion.div>
  );
}
