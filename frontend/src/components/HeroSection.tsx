import { motion } from 'motion/react';
import { Sparkles } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';

export function HeroSection() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden" id="home">
      {/* Background Image with Overlay */}
      <div className="absolute inset-0 z-0">
        <ImageWithFallback
          src="https://images.unsplash.com/photo-1652961221362-4ea2d7af5b40?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBoZGIlMjBpbnRlcmlvciUyMGxpdmluZyUyMHJvb218ZW58MXx8fHwxNzYxODEzNzU4fDA&ixlib=rb-4.1.0&q=80&w=1080"
          alt="Modern HDB Interior"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-white/85 via-white/75 to-[#FAFAF8]/98 backdrop-blur-sm" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(212,115,94,0.15),transparent_50%),radial-gradient(circle_at_bottom_left,rgba(168,181,160,0.15),transparent_50%)]" />
      </div>

      {/* Floating Particles */}
      <div className="absolute inset-0 z-0 overflow-hidden pointer-events-none">
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-[#D4735E]/20 rounded-full"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [0, -30, 0],
              opacity: [0.2, 0.5, 0.2],
            }}
            transition={{
              duration: 3 + Math.random() * 2,
              repeat: Infinity,
              delay: Math.random() * 2,
            }}
          />
        ))}
      </div>

      {/* Content */}
      <div className="relative z-10 container mx-auto px-6 py-20 text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="max-w-4xl mx-auto space-y-8"
        >
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-white/20 backdrop-blur-2xl rounded-full border border-white/30 shadow-xl shadow-black/5"
          >
            <Sparkles className="w-4 h-4 text-[#D4735E]" />
            <span className="text-sm text-gray-900">AI-Powered Interior Design</span>
          </motion.div>

          {/* Main Headline */}
          <h1 className="text-5xl md:text-6xl lg:text-7xl text-gray-900 leading-tight">
            Transform Your HDB
            <br />
            <span className="bg-gradient-to-r from-[#D4735E] to-[#C96A54] bg-clip-text text-transparent">
              Into Your Dream Home
            </span>
          </h1>

          {/* Subheading */}
          <p className="text-xl md:text-2xl text-gray-600 max-w-2xl mx-auto">
            Describe your vision, and let our AI create personalized furniture recommendations tailored to your HDB space
          </p>

          {/* Trust Indicators */}
          <div className="inline-flex items-center gap-8 pt-4 px-8 py-6 bg-white/20 backdrop-blur-2xl border border-white/30 rounded-3xl shadow-xl">
            <div className="text-center">
              <div className="text-2xl text-gray-900">10,000+</div>
              <div className="text-sm text-gray-600">Happy Homeowners</div>
            </div>
            <div className="w-px h-12 bg-white/40" />
            <div className="text-center">
              <div className="text-2xl text-gray-900">50,000+</div>
              <div className="text-sm text-gray-600">Design Ideas</div>
            </div>
            <div className="w-px h-12 bg-white/40" />
            <div className="text-center">
              <div className="text-2xl text-gray-900">4.9★</div>
              <div className="text-sm text-gray-600">User Rating</div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Scroll Indicator */}
      <motion.div
        className="absolute bottom-8 left-1/2 -translate-x-1/2 z-10"
        animate={{ y: [0, 10, 0] }}
        transition={{ duration: 2, repeat: Infinity }}
      >
        <div className="w-6 h-10 border-2 border-gray-400 rounded-full p-1">
          <motion.div
            className="w-1.5 h-1.5 bg-gray-400 rounded-full mx-auto"
            animate={{ y: [0, 20, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
          />
        </div>
      </motion.div>
    </section>
  );
}
