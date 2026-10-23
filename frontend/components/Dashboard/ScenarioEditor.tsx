/**
 * ScenarioEditor Component
 * Interface for creating and configuring disruption scenarios
 * Supports drag-and-drop for road selection and severity configuration
 */

'use client';

import React, { useState } from 'react';

interface ScenarioFormData {
  name: string;
  description: string;
  disruptionType: string;
  severityLevel: number;
  durationMinutes: number;
  affectedRoads: number[];
}

interface ScenarioEditorProps {
  studyAreaId: number;
  onSubmit: (data: ScenarioFormData) => void;
  onCancel: () => void;
}

const disruptionTypes = [
  { value: 'road_closure', label: 'Road Closure' },
  { value: 'accident', label: 'Accident' },
  { value: 'flooding', label: 'Flooding' },
  { value: 'landslide', label: 'Landslide' },
  { value: 'bridge_failure', label: 'Bridge Failure' },
];

const ScenarioEditor: React.FC<ScenarioEditorProps> = ({
  studyAreaId,
  onSubmit,
  onCancel,
}) => {
  const [formData, setFormData] = useState<ScenarioFormData>({
    name: '',
    description: '',
    disruptionType: 'road_closure',
    severityLevel: 1,
    durationMinutes: 60,
    affectedRoads: [],
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]:
        name === 'severityLevel' || name === 'durationMinutes'
          ? parseInt(value)
          : value,
    }));
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Scenario name is required';
    }
    if (formData.name.length > 255) {
      newErrors.name = 'Scenario name must be less than 255 characters';
    }
    if (formData.severityLevel < 1 || formData.severityLevel > 5) {
      newErrors.severityLevel = 'Severity level must be between 1 and 5';
    }
    if (formData.durationMinutes < 1) {
      newErrors.durationMinutes = 'Duration must be at least 1 minute';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-2xl font-bold text-gray-800 mb-6">Create Scenario</h3>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Scenario Name */}
        <div>
          <label htmlFor="name" className="block text-sm font-semibold text-gray-700 mb-2">
            Scenario Name *
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            placeholder="e.g., Bay Bridge Closure"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {errors.name && <p className="text-red-500 text-sm mt-1">{errors.name}</p>}
        </div>

        {/* Description */}
        <div>
          <label htmlFor="description" className="block text-sm font-semibold text-gray-700 mb-2">
            Description
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            placeholder="Detailed description of the scenario..."
            rows={4}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Disruption Type */}
        <div>
          <label htmlFor="disruptionType" className="block text-sm font-semibold text-gray-700 mb-2">
            Disruption Type *
          </label>
          <select
            id="disruptionType"
            name="disruptionType"
            value={formData.disruptionType}
            onChange={handleInputChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {disruptionTypes.map((type) => (
              <option key={type.value} value={type.value}>
                {type.label}
              </option>
            ))}
          </select>
        </div>

        {/* Severity Level */}
        <div>
          <label htmlFor="severityLevel" className="block text-sm font-semibold text-gray-700 mb-2">
            Severity Level: {formData.severityLevel}/5
          </label>
          <input
            type="range"
            id="severityLevel"
            name="severityLevel"
            min="1"
            max="5"
            value={formData.severityLevel}
            onChange={handleInputChange}
            className="w-full"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-2">
            <span>Low</span>
            <span>Moderate</span>
            <span>High</span>
            <span>Critical</span>
            <span>Catastrophic</span>
          </div>
        </div>

        {/* Duration */}
        <div>
          <label htmlFor="durationMinutes" className="block text-sm font-semibold text-gray-700 mb-2">
            Duration (minutes) *
          </label>
          <input
            type="number"
            id="durationMinutes"
            name="durationMinutes"
            value={formData.durationMinutes}
            onChange={handleInputChange}
            min="1"
            max="10080"
            placeholder="60"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {errors.durationMinutes && (
            <p className="text-red-500 text-sm mt-1">{errors.durationMinutes}</p>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex gap-4 pt-4">
          <button
            type="submit"
            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition"
          >
            Create Scenario
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 font-semibold py-2 px-4 rounded-lg transition"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default ScenarioEditor;
