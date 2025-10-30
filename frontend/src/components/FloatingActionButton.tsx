import { motion } from 'motion/react';
import { Plus } from 'lucide-react';

interface FloatingActionButtonProps {
  onClick: () => void;
}

export function FloatingActionButton({ onClick }: FloatingActionButtonProps) {
  return (
    <motion.button
      onClick={onClick}
      className="fixed bottom-8 right-8 w-16 h-16 bg-gradient-to-br from-[#D4735E] to-[#C96A54] text-white rounded-2xl shadow-2xl hover:shadow-3xl z-40 flex items-center justify-center backdrop-blur-xl border border-white/20"
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      initial={{ opacity: 0, scale: 0 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: 1, type: 'spring', stiffness: 200 }}
    >
      <Plus className="w-7 h-7" />
    </motion.button>
  );
}
