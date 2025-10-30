import { useState } from 'react';
import { motion } from 'motion/react';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Sparkles, Loader2, Mic, Home, BedDouble, Lamp, UtensilsCrossed } from 'lucide-react';
import { Badge } from './ui/badge';

interface MainSearchInterfaceProps {
  onSearch: (prompt: string) => void;
  isLoading: boolean;
}

const quickSuggestions = [
  { icon: Home, label: 'Living Room', prompt: 'Modern minimalist living room with Scandinavian vibes' },
  { icon: BedDouble, label: 'Master Bedroom', prompt: 'Cozy master bedroom with warm lighting and natural materials' },
  { icon: Lamp, label: 'Study Area', prompt: 'Productive home office with ergonomic furniture' },
  { icon: UtensilsCrossed, label: 'Dining Space', prompt: 'Elegant dining room for family gatherings' },
];

export function MainSearchInterface({ onSearch, isLoading }: MainSearchInterfaceProps) {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt.trim() && !isLoading) {
      onSearch(prompt.trim());
    }
  };

  const handleSuggestionClick = (suggestionPrompt: string) => {
    setPrompt(suggestionPrompt);
  };

  return (
    <section className="py-20 px-6">
      <div className="container mx-auto max-w-4xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="space-y-8"
        >
          {/* Main Input Card */}
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-[#D4735E]/20 to-[#A8B5A0]/20 rounded-3xl blur-3xl" />
            <div className="relative bg-white/30 backdrop-blur-3xl rounded-3xl border border-white/40 shadow-2xl shadow-black/10 p-8 md:p-12">
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-3">
                  <label htmlFor="design-prompt" className="block text-lg text-gray-700">
                    Describe your dream space
                  </label>
                  <div className="relative">
                    <Textarea
                      id="design-prompt"
                      placeholder="E.g., 'Modern minimalist living room with Scandinavian vibes, lots of natural light, and cozy reading nook...'"
                      value={prompt}
                      onChange={(e) => setPrompt(e.target.value)}
                      className="min-h-[140px] text-lg resize-none bg-white/50 backdrop-blur-xl border-white/40 focus:border-white/60 focus:bg-white/60 rounded-2xl px-6 py-4 pr-14 shadow-inner"
                      disabled={isLoading}
                    />
                    <button
                      type="button"
                      className="absolute right-4 bottom-4 p-2.5 text-gray-600 hover:text-[#D4735E] transition-colors rounded-xl hover:bg-white/60 backdrop-blur-xl"
                      disabled={isLoading}
                    >
                      <Mic className="w-5 h-5" />
                    </button>
                  </div>
                </div>

                <Button
                  type="submit"
                  size="lg"
                  className="w-full h-14 text-lg bg-gradient-to-r from-[#D4735E] to-[#C96A54] hover:from-[#C96A54] hover:to-[#D4735E] text-white rounded-xl shadow-lg hover:shadow-xl transition-all"
                  disabled={!prompt.trim() || isLoading}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      Crafting Your Perfect Space...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-5 h-5 mr-2" />
                      Get Design Ideas
                    </>
                  )}
                </Button>
              </form>
            </div>
          </div>

          {/* Quick Suggestions */}
          <div className="space-y-4">
            <p className="text-center text-gray-600">Or try these popular spaces:</p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {quickSuggestions.map((suggestion, index) => (
                <motion.button
                  key={index}
                  onClick={() => handleSuggestionClick(suggestion.prompt)}
                  disabled={isLoading}
                  whileHover={{ scale: 1.03 }}
                  whileTap={{ scale: 0.98 }}
                  className="flex flex-col items-center gap-3 p-6 bg-white/20 backdrop-blur-2xl border border-white/30 rounded-2xl hover:bg-white/30 hover:border-white/40 hover:shadow-xl shadow-black/5 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <div className="w-12 h-12 bg-white/40 backdrop-blur-xl rounded-xl flex items-center justify-center shadow-lg shadow-black/5">
                    <suggestion.icon className="w-6 h-6 text-[#D4735E]" />
                  </div>
                  <span className="text-sm text-gray-900">{suggestion.label}</span>
                </motion.button>
              ))}
            </div>
          </div>

          {/* Features */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-8">
            <div className="text-center space-y-3 p-6 bg-white/10 backdrop-blur-2xl border border-white/20 rounded-2xl">
              <div className="w-14 h-14 bg-gradient-to-br from-[#D4735E]/20 to-[#D4735E]/10 backdrop-blur-xl rounded-2xl flex items-center justify-center mx-auto shadow-lg shadow-black/5">
                <Sparkles className="w-7 h-7 text-[#D4735E]" />
              </div>
              <h3 className="text-gray-900">AI-Powered</h3>
              <p className="text-sm text-gray-600">Advanced RAG technology for personalized recommendations</p>
            </div>
            <div className="text-center space-y-3 p-6 bg-white/10 backdrop-blur-2xl border border-white/20 rounded-2xl">
              <div className="w-14 h-14 bg-gradient-to-br from-[#A8B5A0]/20 to-[#A8B5A0]/10 backdrop-blur-xl rounded-2xl flex items-center justify-center mx-auto shadow-lg shadow-black/5">
                <Home className="w-7 h-7 text-[#A8B5A0]" />
              </div>
              <h3 className="text-gray-900">HDB Optimized</h3>
              <p className="text-sm text-gray-600">Tailored specifically for Singapore HDB layouts</p>
            </div>
            <div className="text-center space-y-3 p-6 bg-white/10 backdrop-blur-2xl border border-white/20 rounded-2xl">
              <div className="w-14 h-14 bg-gradient-to-br from-[#E8DCC4]/30 to-[#E8DCC4]/10 backdrop-blur-xl rounded-2xl flex items-center justify-center mx-auto shadow-lg shadow-black/5">
                <Badge className="w-7 h-7 text-[#D4735E]" />
              </div>
              <h3 className="text-gray-900">Instant Results</h3>
              <p className="text-sm text-gray-600">Get curated furniture ideas in seconds</p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
