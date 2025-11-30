'use client';

import { Furniture } from '@/types/furniture';
import { CATEGORY_COLORS } from '@/lib/furnitureData';

interface FurnitureItemProps {
  item: Furniture;
  onToggleVisibility: (id: string) => void;
}

/**
 * Individual furniture item card component
 * Displays furniture metadata and visibility toggle
 */
export default function FurnitureItem({ item, onToggleVisibility }: FurnitureItemProps) {
  const categoryColor = CATEGORY_COLORS[item.category];

  // Generate confidence bar width
  const confidenceWidth = `${item.confidenceScore * 100}%`;

  // Format dimensions
  const dimensions = `${item.dimensions.width}×${item.dimensions.depth}×${item.dimensions.height}m`;

  return (
    <div
      className={`
        p-3 rounded-lg border-2 transition-all duration-200
        ${item.visible
          ? 'bg-white border-primary-500 shadow-md'
          : 'bg-gray-50 border-gray-200 opacity-60'
        }
        hover:shadow-lg cursor-pointer
      `}
      onClick={() => onToggleVisibility(item.id)}
    >
      <div className="flex items-start justify-between gap-2">
        {/* Color indicator thumbnail */}
        <div
          className="w-12 h-12 rounded flex-shrink-0 border-2 border-gray-300"
          style={{ backgroundColor: categoryColor }}
          title={item.category}
        />

        {/* Item details */}
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-sm text-gray-900 truncate">
            {item.name}
          </h3>
          <p className="text-xs text-gray-500 capitalize mt-0.5">
            {item.category}
          </p>
          <p className="text-xs text-gray-600 mt-1" title={dimensions}>
            {dimensions}
          </p>
        </div>

        {/* Toggle indicator */}
        <div className="flex-shrink-0">
          <div
            className={`
              w-10 h-5 rounded-full transition-colors duration-200 flex items-center
              ${item.visible ? 'bg-primary-500' : 'bg-gray-300'}
            `}
          >
            <div
              className={`
                w-4 h-4 bg-white rounded-full shadow-md transition-transform duration-200
                ${item.visible ? 'translate-x-5' : 'translate-x-0.5'}
              `}
            />
          </div>
        </div>
      </div>

      {/* Confidence score bar */}
      <div className="mt-3">
        <div className="flex justify-between items-center mb-1">
          <span className="text-xs text-gray-600">Confidence</span>
          <span className="text-xs font-semibold text-gray-900">
            {Math.round(item.confidenceScore * 100)}%
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-1.5">
          <div
            className="bg-primary-600 h-1.5 rounded-full transition-all duration-300"
            style={{ width: confidenceWidth }}
          />
        </div>
      </div>

      {/* Description (if available) */}
      {item.description && (
        <p className="text-xs text-gray-500 mt-2 line-clamp-2">
          {item.description}
        </p>
      )}
    </div>
  );
}
