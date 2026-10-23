'use client';

import Link from 'next/link';
import { ArrowRight, CheckCircle } from 'lucide-react';

export function CTASection() {
  return (
    <section className="py-20 lg:py-32 bg-gradient-to-r from-deep-navy to-teal/20">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-white">
        <h2 className="text-4xl lg:text-5xl font-bold mb-6">
          Ready to Make Data-Driven Decisions?
        </h2>

        <p className="text-xl text-gray-200 mb-12 leading-relaxed">
          Join urban planners, disaster-preparedness teams, and researchers who are using RippleMap AI to build more resilient communities.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
          <Link
            href="/dashboard"
            className="inline-flex items-center justify-center bg-teal hover:bg-teal/90 text-white px-8 py-4 rounded-lg font-semibold transition text-lg"
          >
            Get Started Free <ArrowRight className="ml-2 w-5 h-5" />
          </Link>
          <Link
            href="/docs"
            className="inline-flex items-center justify-center bg-white/10 hover:bg-white/20 text-white px-8 py-4 rounded-lg font-semibold transition text-lg border border-white/20"
          >
            View Documentation
          </Link>
        </div>

        {/* Benefits */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
          <div className="flex flex-col items-center">
            <CheckCircle className="w-8 h-8 text-teal mb-3" />
            <p className="font-semibold">No Credit Card Required</p>
            <p className="text-gray-300 text-sm">Start analyzing immediately</p>
          </div>
          <div className="flex flex-col items-center">
            <CheckCircle className="w-8 h-8 text-teal mb-3" />
            <p className="font-semibold">Research Grade</p>
            <p className="text-gray-300 text-sm">Transparent and reproducible</p>
          </div>
          <div className="flex flex-col items-center">
            <CheckCircle className="w-8 h-8 text-teal mb-3" />
            <p className="font-semibold">Expert Support</p>
            <p className="text-gray-300 text-sm">Community and documentation</p>
          </div>
        </div>
      </div>
    </section>
  );
}
