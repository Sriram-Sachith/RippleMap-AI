'use client';

import { HeroSection } from '@/components/Home/HeroSection';
import { FeaturesSection } from '@/components/Home/FeaturesSection';
import { HowItWorks } from '@/components/Home/HowItWorks';
import { CTASection } from '@/components/Home/CTASection';
import { TestimonialsSection } from '@/components/Home/TestimonialsSection';

export default function Home() {
  return (
    <>
      <HeroSection />
      <FeaturesSection />
      <HowItWorks />
      <TestimonialsSection />
      <CTASection />
    </>
  );
}
