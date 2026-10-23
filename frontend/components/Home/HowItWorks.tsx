'use client';

import { ArrowRight } from 'lucide-react';

const steps = [
  {
    number: '01',
    title: 'Select Study Area',
    description: 'Choose a district or region to analyze. Our platform covers urban and rural areas with detailed road networks.',
  },
  {
    number: '02',
    title: 'Define Scenario',
    description: 'Create a custom disruption scenario by selecting roads and specifying closure parameters.',
  },
  {
    number: '03',
    title: 'Run Simulation',
    description: 'Our analysis engine calculates accessibility changes, population impact, and affected services in real-time.',
  },
  {
    number: '04',
    title: 'Analyze Results',
    description: 'Explore vulnerability rankings, alternative routes, and detailed metrics through interactive visualizations.',
  },
  {
    number: '05',
    title: 'Generate Reports',
    description: 'Export comprehensive reports with methodology, assumptions, and data provenance for stakeholder review.',
  },
];

export function HowItWorks() {
  return (
    <section className="py-20 lg:py-32 bg-mist-blue/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold mb-6 text-deep-navy">
            How It Works
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Five simple steps to understand road disruption impacts
          </p>
        </div>

        <div className="space-y-8">
          {steps.map((step, idx) => (
            <div key={idx} className="relative">
              <div className="flex gap-8">
                {/* Step number */}
                <div className="flex flex-col items-center">
                  <div className="bg-teal text-white w-16 h-16 rounded-full flex items-center justify-center font-bold text-2xl">
                    {step.number}
                  </div>
                  {idx < steps.length - 1 && (
                    <div className="hidden md:block w-1 h-24 bg-gradient-to-b from-teal to-teal/30 mt-4"></div>
                  )}
                </div>

                {/* Content */}
                <div className="pb-8 md:pb-0">
                  <h3 className="text-2xl font-bold mb-3 text-deep-navy">
                    {step.title}
                  </h3>
                  <p className="text-gray-600 text-lg leading-relaxed">
                    {step.description}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Bottom CTA */}
        <div className="mt-16 text-center">
          <a
            href="/dashboard"
            className="inline-flex items-center gap-2 bg-deep-navy hover:bg-deep-navy/90 text-white px-8 py-3 rounded-lg font-semibold transition"
          >
            Try It Now <ArrowRight className="w-5 h-5" />
          </a>
        </div>
      </div>
    </section>
  );
}
