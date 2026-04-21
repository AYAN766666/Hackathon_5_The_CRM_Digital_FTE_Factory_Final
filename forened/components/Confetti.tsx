'use client';

/**
 * Confetti Animation Component
 * Celebration effect for successful ticket creation
 */
import React, { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface ConfettiPiece {
  id: number;
  x: number;
  y: number;
  rotation: number;
  color: string;
  size: number;
  delay: number;
}

interface ConfettiProps {
  isActive: boolean;
  onComplete?: () => void;
}

const COLORS = [
  '#4F8DF7',
  '#28A745',
  '#FFD700',
  '#FF6B6B',
  '#9B59B6',
  '#1ABC9C',
  '#E74C3C',
  '#3498DB',
];

export default function Confetti({ isActive, onComplete }: ConfettiProps) {
  const [confetti, setConfetti] = React.useState<ConfettiPiece[]>([]);

  useEffect(() => {
    if (isActive) {
      // Generate confetti pieces
      const pieces: ConfettiPiece[] = [];
      for (let i = 0; i < 100; i++) {
        pieces.push({
          id: i,
          x: Math.random() * 100,
          y: -10 - Math.random() * 20,
          rotation: Math.random() * 360,
          color: COLORS[Math.floor(Math.random() * COLORS.length)],
          size: Math.random() * 10 + 5,
          delay: Math.random() * 0.5,
        });
      }
      setConfetti(pieces);

      // Auto cleanup after animation
      const timer = setTimeout(() => {
        setConfetti([]);
        onComplete?.();
      }, 3000);

      return () => clearTimeout(timer);
    }
  }, [isActive, onComplete]);

  return (
    <AnimatePresence>
      {isActive && confetti.length > 0 && (
        <div className="fixed inset-0 pointer-events-none z-[100] overflow-hidden">
          {confetti.map((piece) => (
            <motion.div
              key={piece.id}
              initial={{ x: `${piece.x}%`, y: `${piece.y}%`, rotate: 0 }}
              animate={{
                y: '110vh',
                rotate: piece.rotation + 720,
                x: `${piece.x + (Math.random() * 20 - 10)}%`,
              }}
              transition={{
                duration: Math.random() * 2 + 2,
                delay: piece.delay,
                ease: 'linear',
              }}
              style={{
                position: 'absolute',
                width: `${piece.size}px`,
                height: `${piece.size}px`,
                backgroundColor: piece.color,
                borderRadius: Math.random() > 0.5 ? '50%' : '2px',
                boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
              }}
            />
          ))}
        </div>
      )}
    </AnimatePresence>
  );
}
