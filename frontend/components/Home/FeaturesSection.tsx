'use client';

import { Map, Zap, BarChart3, Route, FileText, Shield } from 'lucide-react';

const features = [
  {
    icon: Map,
    title: 'Interactive Map Workspace',
    description: 'Zoom, pan, and filter geographic data in real-time. Multiple layer toggles for roads, hospitals, population, and risk.',
  },
  {
    icon: Zap,
    title: 'Disruption Simulation',
    description: 'Create custom scenarios, simulate road closures instantly, and compare before-and-after accessibility metrics.',
  },
  {
    icon: BarChart3,
    title: 'Vulnerability Analysis',
    description: 'Identify at-risk communities with ranked population exposure and disruption impact metrics.',
  },
  {
    icon: Route,
    title: 'Alternative Routes',
    description: 'Compare service access under disrupted scenarios with travel time and distance analysis.',
  },
  {
    icon: FileText,
    title: 'Advanced Reporting',
    description: 'Export comprehensive reports in CSV and PDF formats with full methodology documentation.',
  },
  {
    icon: Shield,
    title: 'Research Grade',
    description: 'Transparent algorithms, published assumptions, and reproducible results for credible analysis.',
  },
];

export function FeaturesSection() {
  return (
    <section className="py-20 lg:py-32 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold mb-6 text-deep-navy">
            Powerful Features for Better Decisions
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Everything you need to understand road disruptions and their impact on essential services.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, idx) => {
            const Icon = feature.icon;
            return (
              <div
                key={idx}
                className="bg-mist-blue/50 p-8 rounded-lg border border-gray-200 hover:border-teal hover:shadow-hover transition group"
              >
                <div className="bg-teal/20 w-12 h-12 rounded-lg flex items-center justify-center mb-6 group-hover:bg-teal/30 transition">
                  <Icon className="w-6 h-6 text-teal" />
                </div>
                <h3 className="text-lg font-semibold mb-3 text-deep-navy">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
