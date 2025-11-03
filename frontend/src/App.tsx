import { useState } from 'react';
import { Navigation } from './components/Navigation';
import { HeroSection } from './components/HeroSection';
import { MainSearchInterface } from './components/MainSearchInterface';
import { ResultsDisplay } from './components/ResultsDisplay';
import { FilterPanel } from './components/FilterPanel';
import { Footer } from './components/Footer';
import { FloatingActionButton } from './components/FloatingActionButton';
import { getFurnitureRecommendations } from './services/api';
import { RAGResponse } from './types/furniture';
import { Toaster } from './components/ui/sonner';
import { toast } from 'sonner@2.0.3';
import { Progress } from './components/ui/progress';

export default function App() {
  const [results, setResults] = useState<RAGResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isFilterOpen, setIsFilterOpen] = useState(false);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [selectedFurnitureTypes, setSelectedFurnitureTypes] = useState<string[]>([]);
  const [currentPrompt, setCurrentPrompt] = useState<string>('');

  const handleSearch = async (prompt: string, furnitureTypes?: string[]) => {
    setIsLoading(true);
    setError(null);
    setLoadingProgress(0);
    setCurrentPrompt(prompt);

    // Simulate progress
    const progressInterval = setInterval(() => {
      setLoadingProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return prev;
        }
        return prev + 10;
      });
    }, 150);

    try {
      const data = await getFurnitureRecommendations(prompt, furnitureTypes || selectedFurnitureTypes);
      setResults(data);
      setLoadingProgress(100);
      toast.success(`Found ${data.totalResults} perfect furniture pieces!`, {
        description: 'Scroll down to explore your personalized recommendations',
      });

      // Smooth scroll to results
      setTimeout(() => {
        document.getElementById('results')?.scrollIntoView({
          behavior: 'smooth',
          block: 'start',
        });
      }, 300);
    } catch (err) {
      const errorMessage = 'Unable to fetch recommendations. Please check your connection.';
      setError(errorMessage);
      toast.error('Oops! Something went wrong', {
        description: errorMessage,
      });
      console.error('Search error:', err);
    } finally {
      setIsLoading(false);
      clearInterval(progressInterval);
      setTimeout(() => setLoadingProgress(0), 1000);
    }
  };

  const handleNewConsultation = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    setResults(null);
    setError(null);
    setSelectedFurnitureTypes([]);
    setCurrentPrompt('');
  };

  const handleFurnitureTypeToggle = (type: string) => {
    setSelectedFurnitureTypes((prev) => {
      if (prev.includes(type)) {
        return prev.filter((t) => t !== type);
      }
      return [...prev, type];
    });
  };

  const handleApplyFilters = () => {
    if (currentPrompt) {
      handleSearch(currentPrompt, selectedFurnitureTypes);
      setIsFilterOpen(false);
    } else {
      toast.info('Please enter a search prompt first', {
        description: 'Describe your dream space to get started',
      });
    }
  };

  const handleResetFilters = () => {
    setSelectedFurnitureTypes([]);
    if (currentPrompt) {
      handleSearch(currentPrompt, []);
    }
    toast.info('Filters reset', {
      description: 'Showing all furniture types',
    });
  };

  const handleRefresh = () => {
    toast.info('Refining your results...', {
      description: 'Adjust filters to see different options',
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#FAFAF8] via-[#F5F5F3] to-[#E8DCC4]/20 relative">
      {/* Gradient Orbs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 right-1/4 w-96 h-96 bg-[#D4735E]/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-[#A8B5A0]/10 rounded-full blur-3xl" />
        <div className="absolute top-1/3 right-1/3 w-96 h-96 bg-[#E8DCC4]/20 rounded-full blur-3xl" />
      </div>

      {/* Toast Notifications */}
      <Toaster position="top-right" richColors />

      {/* Loading Progress Bar */}
      {isLoading && (
        <div className="fixed top-0 left-0 right-0 z-50">
          <Progress value={loadingProgress} className="h-1 rounded-none" />
        </div>
      )}

      {/* Navigation */}
      <Navigation />

      {/* Hero Section */}
      <HeroSection />

      {/* Main Search Interface */}
      <MainSearchInterface onSearch={handleSearch} isLoading={isLoading} />

      {/* Results Display */}
      <ResultsDisplay
        results={results}
        error={error}
        onFilterClick={() => setIsFilterOpen(true)}
        onRefresh={handleRefresh}
        activeFiltersCount={selectedFurnitureTypes.length}
      />

      {/* Filter Panel */}
      <FilterPanel
        isOpen={isFilterOpen}
        onClose={() => setIsFilterOpen(false)}
        selectedFurnitureTypes={selectedFurnitureTypes}
        onFurnitureTypeToggle={handleFurnitureTypeToggle}
        onApplyFilters={handleApplyFilters}
        onResetFilters={handleResetFilters}
      />

      {/* Floating Action Button */}
      {results && <FloatingActionButton onClick={handleNewConsultation} />}

      {/* Footer */}
      <Footer />
    </div>
  );
}
