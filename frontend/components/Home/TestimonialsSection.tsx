'use client';

import { Quote } from 'lucide-react';

const testimonials = [
  {
    quote: 'RippleMap AI provided critical insights for our disaster preparedness planning. The vulnerability rankings helped us prioritize interventions.',
    author: 'Dr. Asha Patel',
    role: 'District Planner, Karnataka',
  },
  {
    quote: 'The transparency of the methodology and reproducible results make this a credible tool for research and policy decisions.',
    author: 'Prof. Rajesh Kumar',
    role: 'Transport Researcher, University of Delhi',
  },
  {
    quote: 'Being able to simulate scenarios before they happen allows us to prepare better. The data exports are excellent for stakeholder engagement.',
    author: 'Maria Santos',
    role: 'NGO Director, Community Resilience',
  },
];

export function TestimonialsSection() {
  return (
    <section className="py-20 lg:py-32 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold mb-6 text-deep-navy">
            Trusted by Leaders
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Hear from urban planners, researchers, and community leaders
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, idx) => (
            <div
              key={idx}
              className="bg-mist-blue/50 p-8 rounded-lg border border-gray-200 hover:border-teal hover:shadow-hover transition"
            >
              <Quote className="w-8 h-8 text-teal mb-4" />
              <p className="text-gray-700 mb-6 leading-relaxed italic">
                "{testimonial.quote}"
              </p>
              <div>
                <p className="font-semibold text-deep-navy">{testimonial.author}</p>
                <p className="text-gray-600 text-sm">{testimonial.role}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
