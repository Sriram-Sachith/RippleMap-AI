/**
 * MetricsPanel Component
 * Real-time display of key analysis metrics and KPIs
 * Updates dynamically as scenarios are analyzed
 */

'use client';

import React from 'react';

interface MetricCard {
  title: string;
  value: string | number;
  unit?: string;
  icon: string;
  color: 'blue' | 'red' | 'green' | 'yellow' | 'purple';
  change?: number;
}

interface MetricsPanelProps {
  metrics: MetricCard[];
  isLoading?: boolean;
}

const colorClasses = {
  blue: 'bg-blue-50 border-blue-200 text-blue-700',
  red: 'bg-red-50 border-red-200 text-red-700',
  green: 'bg-green-50 border-green-200 text-green-700',
  yellow: 'bg-yellow-50 border-yellow-200 text-yellow-700',
  purple: 'bg-purple-50 border-purple-200 text-purple-700',
};

const MetricsPanel: React.FC<MetricsPanelProps> = ({ metrics, isLoading = false }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {metrics.map((metric, idx) => (
        <div
          key={idx}
          className={`border-l-4 rounded-lg p-6 transition-all ${colorClasses[metric.color]}`}
        >
          <div className="flex items-start justify-between mb-4">
            <div className="text-2xl">{metric.icon}</div>
            {metric.change !== undefined && (
              <span
                className={`text-sm font-semibold px-2 py-1 rounded ${
                  metric.change >= 0
                    ? 'bg-green-200 text-green-800'
                    : 'bg-red-200 text-red-800'
                }`}
              >
                {metric.change >= 0 ? '+' : ''}{metric.change}%
              </span>
            )}
          </div>

          <p className="text-gray-600 text-sm font-medium mb-2">{metric.title}</p>

          {isLoading ? (
            <div className="h-8 bg-gray-300 animate-pulse rounded"></div>
          ) : (
            <p className="text-3xl font-bold">
              {metric.value}
              {metric.unit && <span className="text-lg text-gray-600 ml-1">{metric.unit}</span>}
            </p>
          )}
        </div>
      ))}
    </div>
  );
};

export default MetricsPanel;
