import { useRef } from 'react';
import { FurnitureItem } from '../types/furniture';
import { motion, useScroll, useTransform } from 'motion/react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { Badge } from './ui/badge';
import { Ruler, Package, Palette, Star, TrendingUp } from 'lucide-react';
import { Button } from './ui/button';

interface DesignCardProps {
  item: FurnitureItem;
  index: number;
}

export function DesignCard({ item, index }: DesignCardProps) {
  const cardRef = useRef<HTMLDivElement>(null);

  const { scrollYProgress } = useScroll({
    target: cardRef,
    offset: ["start end", "end start"]
  });

  const rotateX = useTransform(scrollYProgress, [0, 0.5, 1], [8, 0, -8]);
  const rotateY = useTransform(scrollYProgress, [0, 0.5, 1], [-5, 0, 5]);
  const scale = useTransform(scrollYProgress, [0, 0.3, 0.7, 1], [0.9, 1, 1, 0.9]);
  const opacity = useTransform(scrollYProgress, [0, 0.2, 0.8, 1], [0.4, 1, 1, 0.4]);

  return (
    <motion.div
      ref={cardRef}
      style={{
        rotateX,
        rotateY,
        scale,
        opacity,
        transformStyle: "preserve-3d",
      }}
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.6,
        delay: index * 0.1,
        ease: "easeOut"
      }}
      className="group"
    >
      <div className="relative bg-white/25 backdrop-blur-3xl rounded-3xl border border-white/30 overflow-hidden hover:bg-white/35 hover:border-white/40 hover:shadow-2xl shadow-xl shadow-black/10 transition-all duration-500 h-full">
        {/* Image Container */}
        <div className="relative aspect-[4/3] overflow-hidden bg-gradient-to-br from-gray-100/50 to-gray-50/50">
          <ImageWithFallback
            src={item.imageUrl}
            alt={item.name}
            className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
          
          {/* Relevance Badge */}
          {item.relevanceScore && (
            <div className="absolute top-4 right-4 bg-white/30 backdrop-blur-2xl rounded-full px-3 py-1.5 flex items-center gap-1.5 shadow-xl border border-white/40">
              <Star className="w-4 h-4 text-amber-500 fill-current" />
              <span className="text-sm text-gray-900">{(item.relevanceScore * 100).toFixed(0)}% Match</span>
            </div>
          )}
        </div>

        {/* Content */}
        <div className="p-6 space-y-4">
          {/* Title & Badges */}
          <div className="space-y-3">
            <h3 className="text-xl text-gray-900 line-clamp-1 group-hover:text-[#D4735E] transition-colors">
              {item.name}
            </h3>
            <div className="flex gap-2 flex-wrap">
              <Badge className="bg-[#D4735E]/10 text-[#D4735E] border-[#D4735E]/20 hover:bg-[#D4735E]/20">
                {item.category}
              </Badge>
              <Badge variant="outline" className="border-[#A8B5A0]/30 text-[#A8B5A0]">
                {item.style}
              </Badge>
            </div>
          </div>

          {/* Description */}
          <p className="text-gray-600 line-clamp-2 leading-relaxed">
            {item.description}
          </p>

          {/* Details */}
          <div className="space-y-2 text-sm text-gray-600">
            {item.dimensions && (
              <div className="flex items-center gap-2">
                <Ruler className="w-4 h-4 text-[#A8B5A0]" />
                <span>{item.dimensions}</span>
              </div>
            )}
            {item.material && (
              <div className="flex items-center gap-2">
                <Package className="w-4 h-4 text-[#A8B5A0]" />
                <span>{item.material}</span>
              </div>
            )}
            {item.color && (
              <div className="flex items-center gap-2">
                <Palette className="w-4 h-4 text-[#A8B5A0]" />
                <span>{item.color}</span>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="pt-4 border-t border-gray-200/50 flex items-center justify-between">
            <div>
              {/* <div className="text-sm text-gray-500">Starting from</div>
              <div className="text-2xl text-gray-900">${item.price.toFixed(2)}</div> */}
            </div>
            <Button
              size="sm"
              className="bg-gradient-to-r from-[#D4735E] to-[#C96A54] hover:from-[#C96A54] hover:to-[#D4735E] text-white rounded-xl"
            >
              View Details
            </Button>
          </div>
        </div>

        {/* Complexity Indicator */}
        <div className="absolute top-4 left-4 bg-white/30 backdrop-blur-2xl rounded-full px-3 py-1 flex items-center gap-1.5 shadow-xl border border-white/40">
          <TrendingUp className="w-3.5 h-3.5 text-[#A8B5A0]" />
          <span className="text-xs text-gray-900">Easy Setup</span>
        </div>
      </div>
    </motion.div>
  );
}
