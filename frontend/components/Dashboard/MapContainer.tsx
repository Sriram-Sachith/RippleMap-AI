/**
 * MapContainer Component
 * Interactive geospatial map for visualizing road networks, facilities, and analysis results
 * Uses Leaflet for mapping with real-time layer management
 */

'use client';

import React, { useEffect, useRef, useState } from 'react';
import L from 'leaflet';

interface MapContainerProps {
  center?: [number, number];
  zoom?: number;
  onMapReady?: (map: L.Map) => void;
}

const MapContainer: React.FC<MapContainerProps> = ({
  center = [37.7749, -122.4194],
  zoom = 11,
  onMapReady,
}) => {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!mapRef.current) return;

    // Initialize map
    const map = L.map(mapRef.current).setView(center, zoom);

    // Add base layer (OpenStreetMap)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19,
    }).addTo(map);

    // Store reference and notify parent
    mapInstanceRef.current = map;
    setIsLoading(false);

    if (onMapReady) {
      onMapReady(map);
    }

    return () => {
      map.remove();
    };
  }, [center, zoom, onMapReady]);

  return (
    <div className="relative w-full h-full">
      <div
        ref={mapRef}
        className="w-full h-full rounded-lg shadow-lg"
        style={{ minHeight: '600px' }}
      />
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-70 rounded-lg">
          <div className="text-center">
            <div className="w-8 h-8 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-2"></div>
            <p className="text-gray-600">Loading map...</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default MapContainer;
