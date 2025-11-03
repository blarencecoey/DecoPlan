import { motion, AnimatePresence } from 'motion/react';
import { X, SlidersHorizontal, DollarSign, Home, Palette, Armchair } from 'lucide-react';
import { Button } from './ui/button';
import { Label } from './ui/label';
import { Slider } from './ui/slider';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';

interface FilterPanelProps {
  isOpen: boolean;
  onClose: () => void;
  selectedFurnitureTypes?: string[];
  onFurnitureTypeToggle?: (type: string) => void;
  onApplyFilters?: () => void;
  onResetFilters?: () => void;
}

const roomTypes = ['Living Room', 'Bedroom', 'Kitchen', 'Dining', 'Study', 'Bathroom'];
const styles = ['Modern', 'Scandinavian', 'Japanese', 'Industrial', 'Bohemian', 'Minimalist'];
const flatSizes = ['2-Room', '3-Room', '4-Room', '5-Room', 'Executive'];
const furnitureTypes = ['Sofa', 'Chair', 'Armchair', 'Table', 'Dining Table', 'Coffee Table', 'Desk', 'Bed', 'Wardrobe', 'Dresser', 'Bookshelf', 'Cabinet', 'Nightstand', 'Bench', 'Stool', 'Recliner'];

export function FilterPanel({
  isOpen,
  onClose,
  selectedFurnitureTypes = [],
  onFurnitureTypeToggle,
  onApplyFilters,
  onResetFilters
}: FilterPanelProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40"
          />

          {/* Panel */}
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="fixed right-0 top-0 bottom-0 w-full max-w-md bg-white/20 backdrop-blur-3xl border-l border-white/30 shadow-2xl z-50 overflow-y-auto"
          >
            <div className="p-6 space-y-6">
              {/* Header */}
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <SlidersHorizontal className="w-5 h-5 text-[#D4735E]" />
                  <h2 className="text-xl text-gray-900">Refine Your Search</h2>
                  {selectedFurnitureTypes.length > 0 && (
                    <Badge className="bg-[#D4735E] text-white">
                      {selectedFurnitureTypes.length} selected
                    </Badge>
                  )}
                </div>
                <Button variant="ghost" size="icon" onClick={onClose} className="rounded-full">
                  <X className="w-5 h-5" />
                </Button>
              </div>

              <Separator />

              {/* Furniture Type */}
              <div className="space-y-3">
                <Label className="flex items-center gap-2">
                  <Armchair className="w-4 h-4 text-[#A8B5A0]" />
                  Furniture Type
                </Label>
                <div className="flex flex-wrap gap-2">
                  {furnitureTypes.map((type) => (
                    <Badge
                      key={type}
                      variant="outline"
                      onClick={() => onFurnitureTypeToggle?.(type)}
                      className={`cursor-pointer transition-all ${
                        selectedFurnitureTypes.includes(type)
                          ? 'bg-[#D4735E]/20 border-[#D4735E] text-[#D4735E]'
                          : 'bg-white/20 backdrop-blur-xl border-white/30 hover:bg-white/40 hover:border-white/50'
                      }`}
                    >
                      {type}
                    </Badge>
                  ))}
                </div>
              </div>

              <Separator />

              {/* Room Type */}
              <div className="space-y-3">
                <Label className="flex items-center gap-2">
                  <Home className="w-4 h-4 text-[#A8B5A0]" />
                  Room Type
                </Label>
                <div className="flex flex-wrap gap-2">
                  {roomTypes.map((room) => (
                    <Badge
                      key={room}
                      variant="outline"
                      className="cursor-pointer bg-white/20 backdrop-blur-xl border-white/30 hover:bg-white/40 hover:border-white/50 transition-colors"
                    >
                      {room}
                    </Badge>
                  ))}
                </div>
              </div>

              <Separator />

              {/* Style Preference */}
              <div className="space-y-3">
                <Label className="flex items-center gap-2">
                  <Palette className="w-4 h-4 text-[#A8B5A0]" />
                  Style Preference
                </Label>
                <div className="flex flex-wrap gap-2">
                  {styles.map((style) => (
                    <Badge
                      key={style}
                      variant="outline"
                      className="cursor-pointer bg-white/20 backdrop-blur-xl border-white/30 hover:bg-white/40 hover:border-white/50 transition-colors"
                    >
                      {style}
                    </Badge>
                  ))}
                </div>
              </div>

              <Separator />

              {/* Budget Range */}
              <div className="space-y-4">
                <Label className="flex items-center gap-2">
                  <DollarSign className="w-4 h-4 text-[#A8B5A0]" />
                  Budget Range
                </Label>
                <div className="px-2">
                  <Slider
                    defaultValue={[500, 5000]}
                    max={10000}
                    step={100}
                    className="w-full"
                  />
                  <div className="flex justify-between mt-2 text-sm text-gray-600">
                    <span>$500</span>
                    <span>$10,000</span>
                  </div>
                </div>
              </div>

              <Separator />

              {/* Flat Size */}
              <div className="space-y-3">
                <Label className="flex items-center gap-2">
                  <Home className="w-4 h-4 text-[#A8B5A0]" />
                  HDB Flat Size
                </Label>
                <div className="flex flex-wrap gap-2">
                  {flatSizes.map((size) => (
                    <Badge
                      key={size}
                      variant="outline"
                      className="cursor-pointer bg-white/20 backdrop-blur-xl border-white/30 hover:bg-white/40 hover:border-white/50 transition-colors"
                    >
                      {size}
                    </Badge>
                  ))}
                </div>
              </div>

              {/* Actions */}
              <div className="pt-6 space-y-3">
                <Button
                  onClick={onApplyFilters}
                  className="w-full bg-gradient-to-r from-[#D4735E] to-[#C96A54] hover:from-[#C96A54] hover:to-[#D4735E] text-white"
                >
                  Apply Filters
                </Button>
                <Button
                  variant="outline"
                  onClick={onResetFilters}
                  className="w-full"
                >
                  Reset All
                </Button>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
