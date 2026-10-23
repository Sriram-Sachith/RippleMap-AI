'use client';

import Link from 'next/link';
import { useState } from 'react';
import { Menu, X, Map } from 'lucide-react';

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-deep-navy text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 font-bold text-xl">
            <Map className="w-8 h-8 text-teal" />
            <span>RippleMap AI</span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex gap-8">
            <Link href="/" className="hover:text-teal transition">Home</Link>
            <Link href="/dashboard" className="hover:text-teal transition">Dashboard</Link>
            <Link href="/features" className="hover:text-teal transition">Features</Link>
            <Link href="/docs" className="hover:text-teal transition">Documentation</Link>
            <Link href="/about" className="hover:text-teal transition">About</Link>
          </div>

          {/* CTA Button */}
          <Link
            href="/dashboard"
            className="hidden md:inline-block bg-teal hover:bg-teal/90 px-6 py-2 rounded-lg font-semibold transition"
          >
            Get Started
          </Link>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden"
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isOpen && (
          <div className="md:hidden pb-4 space-y-4">
            <Link href="/" className="block hover:text-teal transition">Home</Link>
            <Link href="/dashboard" className="block hover:text-teal transition">Dashboard</Link>
            <Link href="/features" className="block hover:text-teal transition">Features</Link>
            <Link href="/docs" className="block hover:text-teal transition">Documentation</Link>
            <Link href="/about" className="block hover:text-teal transition">About</Link>
            <Link
              href="/dashboard"
              className="block bg-teal hover:bg-teal/90 px-6 py-2 rounded-lg font-semibold transition text-center"
            >
              Get Started
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
}
