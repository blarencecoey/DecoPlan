'use client';

import { Furniture } from '@/types/furniture';
import FurnitureItem from './FurnitureItem';
import { calculateRoomCoverage } from '@/lib/mockRAG';

interface FurniturePanelProps {
  furniture: Furniture[];
  onToggleFurniture: (id: string) => void;
  onRetrieveFurniture: () => void;
  isLoading: boolean;
}

/**
 * Sidebar panel component displaying retrieved furniture items
 * Includes controls for retrieval and statistics display
 */
export default function FurniturePanel({
  furniture,
  onToggleFurniture,
  onRetrieveFurniture,
  isLoading,
}: FurniturePanelProps) {
  // Calculate room statistics
  const stats = calculateRoomCoverage(furniture, 10, 8);
  const visibleCount = furniture.filter(f => f.visible).length;

  return (
    <div className="h-full flex flex-col bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 text-white p-4 shadow-lg">
        <h2 className="text-xl font-bold mb-1">DecoPlan</h2>
        <p className="text-sm text-primary-100">RAG Furniture Retrieval</p>
      </div>

      {/* Control buttons */}
      <div className="p-4 bg-white border-b border-gray-200">
        <button
          onClick={onRetrieveFurniture}
          disabled={isLoading}
          className={`
            w-full py-3 px-4 rounded-lg font-semibold text-white
            transition-all duration-200 flex items-center justify-center gap-2
            ${isLoading
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-primary-600 hover:bg-primary-700 active:scale-95 shadow-md hover:shadow-lg'
            }
          `}
        >
          {isLoading ? (
            <>
              <div className="w-5 h-5 border-3 border-white border-t-transparent rounded-full animate-spin" />
              <span>Retrieving...</span>
            </>
          ) : (
            <>
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
              <span>Retrieve Furniture</span>
            </>
          )}
        </button>
      </div>

      {/* Statistics */}
      {furniture.length > 0 && (
        <div className="p-4 bg-gradient-to-r from-primary-50 to-blue-50 border-b border-primary-100">
          <div className="grid grid-cols-3 gap-2 text-center">
            <div>
              <div className="text-2xl font-bold text-primary-700">
                {visibleCount}
              </div>
              <div className="text-xs text-gray-600">Visible</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-primary-700">
                {stats.coveragePercentage}%
              </div>
              <div className="text-xs text-gray-600">Coverage</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-primary-700">
                {stats.totalFootprint}m²
              </div>
              <div className="text-xs text-gray-600">Footprint</div>
            </div>
          </div>
        </div>
      )}

      {/* Furniture list */}
      <div className="flex-1 overflow-y-auto p-4">
        {furniture.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-gray-400 mb-3">
              <svg
                className="w-16 h-16 mx-auto"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
                />
              </svg>
            </div>
            <p className="text-gray-500 text-sm">No furniture retrieved yet</p>
            <p className="text-gray-400 text-xs mt-1">
              Click &quot;Retrieve Furniture&quot; to start
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-semibold text-gray-700">
                Retrieved Items ({furniture.length})
              </h3>
              <button
                onClick={() => {
                  // Toggle all furniture visibility
                  const allVisible = furniture.every(f => f.visible);
                  furniture.forEach(f => {
                    if (allVisible !== f.visible) {
                      onToggleFurniture(f.id);
                    }
                  });
                }}
                className="text-xs text-primary-600 hover:text-primary-700 font-medium"
              >
                {furniture.every(f => f.visible) ? 'Hide All' : 'Show All'}
              </button>
            </div>
            {furniture.map(item => (
              <FurnitureItem
                key={item.id}
                item={item}
                onToggleVisibility={onToggleFurniture}
              />
            ))}
          </div>
        )}
      </div>

      {/* Footer info */}
      <div className="p-3 bg-white border-t border-gray-200">
        <p className="text-xs text-gray-500 text-center">
          Click on items to toggle visibility in 3D view
        </p>
      </div>
    </div>
  );
}
