/**
 * Sentiment Emoji Helper
 * Maps sentiment scores to emojis and colors
 */

export interface SentimentInfo {
  emoji: string;
  label: string;
  color: string;
  bgColor: string;
}

export function getSentimentInfo(score?: number | null): SentimentInfo {
  if (score === undefined || score === null) {
    return {
      emoji: '😐',
      label: 'Neutral',
      color: 'text-gray-700',
      bgColor: 'bg-gray-100',
    };
  }

  if (score > 0.7) {
    return {
      emoji: '🎉',
      label: 'Very Positive',
      color: 'text-green-700',
      bgColor: 'bg-green-100',
    };
  } else if (score > 0.5) {
    return {
      emoji: '😊',
      label: 'Positive',
      color: 'text-green-700',
      bgColor: 'bg-green-100',
    };
  } else if (score > 0.3) {
    return {
      emoji: '😐',
      label: 'Neutral',
      color: 'text-yellow-700',
      bgColor: 'bg-yellow-100',
    };
  } else if (score > 0.1) {
    return {
      emoji: '😟',
      label: 'Negative',
      color: 'text-orange-700',
      bgColor: 'bg-orange-100',
    };
  } else {
    return {
      emoji: '😠',
      label: 'Very Negative',
      color: 'text-red-700',
      bgColor: 'bg-red-100',
    };
  }
}
