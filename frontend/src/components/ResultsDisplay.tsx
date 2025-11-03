import { motion } from 'motion/react';
import { RAGResponse } from '../types/furniture';
import { DesignCard } from './DesignCard';
import { Clock, Search, SlidersHorizontal, RefreshCw } from 'lucide-react';
import { Alert, AlertDescription } from './ui/alert';
import { Button } from './ui/button';
import { Badge } from './ui/badge';

interface ResultsDisplayProps {
  results: RAGResponse | null;
  error: string | null;
  onFilterClick: () => void;
  onRefresh: () => void;
  activeFiltersCount?: number;
}

export function ResultsDisplay({ results, error, onFilterClick, onRefresh, activeFiltersCount = 0 }: ResultsDisplayProps) {
  if (error) {
    return (
      <section className="py-12 px-6">
        <div className="container mx-auto max-w-4xl">
          <Alert variant="destructive" className="bg-red-500/10 backdrop-blur-2xl border-red-500/30">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        </div>
      </section>
    );
  }

  if (!results) {
    return (
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-3xl text-center space-y-6">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            className="p-12 bg-white/20 backdrop-blur-3xl border border-white/30 rounded-3xl shadow-xl"
          >
            <div className="w-24 h-24 bg-gradient-to-br from-[#D4735E]/20 to-[#A8B5A0]/20 backdrop-blur-xl rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-lg">
              <Search className="w-12 h-12 text-[#D4735E]" />
            </div>
            <h3 className="text-2xl text-gray-900 mb-3">Start Your Design Journey</h3>
            <p className="text-lg text-gray-600">
              Tell us about your dream space and we'll find the perfect furniture pieces for you
            </p>
          </motion.div>
        </div>
      </section>
    );
  }

  return (
    <section className="py-12 px-6" id="results">
      <div className="container mx-auto max-w-7xl space-y-8">
        {/* Results Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between flex-wrap gap-4"
        >
          <div className="space-y-1">
            <h2 className="text-3xl text-gray-900">
              Design Ideas for <span className="text-[#D4735E]">"{results.query}"</span>
            </h2>
            <div className="flex items-center gap-4 text-gray-600">
              <span>{results.totalResults} items found</span>
              {results.processingTime && (
                <span className="flex items-center gap-1.5">
                  <Clock className="w-4 h-4" />
                  {results.processingTime.toFixed(2)}s
                </span>
              )}
            </div>
          </div>

          <div className="flex gap-3">
            <Button
              variant="outline"
              onClick={onRefresh}
              className="bg-white/20 backdrop-blur-2xl border-white/30 hover:bg-white/40 hover:border-white/50"
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              Refine Results
            </Button>
            <Button
              onClick={onFilterClick}
              className="bg-gradient-to-r from-[#D4735E] to-[#C96A54] hover:from-[#C96A54] hover:to-[#D4735E] text-white shadow-lg shadow-[#D4735E]/30 backdrop-blur-xl relative"
            >
              <SlidersHorizontal className="w-4 h-4 mr-2" />
              Filters
              {activeFiltersCount > 0 && (
                <Badge className="ml-2 bg-white text-[#D4735E] hover:bg-white">
                  {activeFiltersCount}
                </Badge>
              )}
            </Button>
          </div>
        </motion.div>

        {/* Results Grid */}
        {results.recommendations.length === 0 ? (
          <div className="text-center py-20">
            <div className="w-20 h-20 bg-white/20 backdrop-blur-2xl border border-white/30 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
              <Search className="w-10 h-10 text-gray-600" />
            </div>
            <h3 className="text-xl text-gray-900 mb-2">No Results Found</h3>
            <p className="text-gray-600">
              Try adjusting your search or use different keywords
            </p>
          </div>
        ) : (
          <div
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
            style={{ perspective: "2000px" }}
          >
            {results.recommendations.map((item, index) => (
              <DesignCard key={item.id} item={item} index={index} />
            ))}
          </div>
        )}

        {/* Load More (Optional) */}
        {results.recommendations.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="text-center pt-8"
          >
            <Button
              variant="outline"
              size="lg"
              className="bg-white/20 backdrop-blur-2xl border-white/30 hover:bg-white/40 hover:border-white/50"
            >
              Load More Designs
            </Button>
          </motion.div>
        )}
      </div>
    </section>
  );
}
