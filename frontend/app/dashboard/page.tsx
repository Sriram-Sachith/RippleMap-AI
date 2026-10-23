'use client';

import React, { useState } from 'react';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import { DashboardLayout } from '@/components/Dashboard/DashboardLayout';
import { ControlPanel } from '@/components/Dashboard/ControlPanel';
import { MetricsPanel } from '@/components/Dashboard/MetricsPanel';
import { useStudyAreas } from '@/hooks/useStudyAreas';
import 'leaflet/dist/leaflet.css';

export default function Dashboard() {
  const { data: studyAreas, isLoading } = useStudyAreas();
  const [selectedArea, setSelectedArea] = useState<string | null>(null);
  const [scenarioParams, setScenarioParams] = useState({});

  return (
    <DashboardLayout>
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-[calc(100vh-120px)]">
        {/* Control Panel */}
        <div className="lg:col-span-1 overflow-y-auto">
          <ControlPanel
            studyAreas={studyAreas}
            selectedArea={selectedArea}
            onAreaSelect={setSelectedArea}
            onScenarioChange={setScenarioParams}
          />
        </div>

        {/* Main Map Area */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-card h-full overflow-hidden">
            <MapContainer
              center={[15.2993, 75.7397]}
              zoom={10}
              style={{ height: '100%', width: '100%' }}
            >
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; OpenStreetMap contributors'
              />
            </MapContainer>
          </div>
        </div>

        {/* Metrics Panel */}
        <div className="lg:col-span-1 overflow-y-auto">
          <MetricsPanel
            selectedArea={selectedArea}
            scenarioParams={scenarioParams}
          />
        </div>
      </div>
    </DashboardLayout>
  );
}
