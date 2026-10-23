'use client';

import Link from 'next/link';
import { ArrowRight, Map, AlertCircle, Users } from 'lucide-react';

export function HeroSection() {
  return (
    <div className="relative overflow-hidden bg-gradient-to-br from-deep-navy via-deep-navy to-teal/20 text-white">
      {/* Background decoration */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-20 left-10 w-72 h-72 bg-teal rounded-full mix-blend-multiply filter blur-3xl"></div>
        <div className="absolute -bottom-8 right-10 w-72 h-72 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl"></div>
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-32">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left content */}
          <div>
            <span className="inline-block bg-teal/20 text-teal px-4 py-1 rounded-full text-sm font-semibold mb-6">
              🌍 Geospatial Intelligence
            </span>

            <h1 className="text-5xl lg:text-6xl font-bold mb-6 leading-tight">
              See the Impact.
              <span className="block text-teal">Find the Vulnerable.</span>
              Plan the Response.
            </h1>

            <p className="text-xl text-gray-300 mb-8 leading-relaxed">
              RippleMap AI combines geographic data, road-network analysis, and population intelligence to help communities understand how disruptions affect essential services.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 mb-12">
              <Link
                href="/dashboard"
                className="inline-flex items-center justify-center bg-teal hover:bg-teal/90 text-white px-8 py-3 rounded-lg font-semibold transition"
              >
                Get Started <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
              <Link
                href="/docs"
                className="inline-flex items-center justify-center bg-white/10 hover:bg-white/20 text-white px-8 py-3 rounded-lg font-semibold transition border border-white/20"
              >
                Learn More
              </Link>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-6">
              <div>
                <div className="text-3xl font-bold text-teal">1M+</div>
                <p className="text-gray-400 text-sm">People Analyzed</p>
              </div>
              <div>
                <div className="text-3xl font-bold text-teal">50K+</div>
                <p className="text-gray-400 text-sm">Roads Mapped</p>
              </div>
              <div>
                <div className="text-3xl font-bold text-teal">99%</div>
                <p className="text-gray-400 text-sm">Data Accuracy</p>
              </div>
            </div>
          </div>

          {/* Right visual */}
          <div className="hidden lg:block">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-teal to-blue-500 rounded-2xl opacity-20 blur-2xl"></div>
              <div className="relative bg-mist-blue/20 rounded-2xl p-8 border border-white/10 backdrop-blur">
                <div className="space-y-4">
                  <div className="flex items-start gap-4">
                    <div className="bg-teal p-3 rounded-lg">
                      <Map className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold">Interactive Map</h3>
                      <p className="text-gray-400 text-sm">Real-time geospatial analysis</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-4">
                    <div className="bg-amber p-3 rounded-lg">
                      <AlertCircle className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold">Vulnerability Ranking</h3>
                      <p className="text-gray-400 text-sm">Identify at-risk areas</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-4">
                    <div className="bg-teal p-3 rounded-lg">
                      <Users className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold">Community Impact</h3>
                      <p className="text-gray-400 text-sm">Data-driven decisions</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
