import { Home, Image, Info, Mail, User } from 'lucide-react';
import { Button } from './ui/button';

export function Navigation() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white/30 backdrop-blur-2xl border-b border-white/20 shadow-lg shadow-black/5">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-gradient-to-br from-[#D4735E] to-[#C96A54] rounded-xl flex items-center justify-center shadow-lg shadow-[#D4735E]/20">
              <span className="text-white font-semibold">D</span>
            </div>
            <span className="text-xl text-gray-900">Homemah</span>
          </div>

          {/* Menu Items */}
          <div className="hidden md:flex items-center gap-2">
            <a href="#home" className="px-4 py-2 text-gray-700 hover:text-gray-900 hover:bg-white/40 backdrop-blur-xl rounded-xl transition-all flex items-center gap-2">
              <Home className="w-4 h-4" />
              <span>Home</span>
            </a>
            <a href="#gallery" className="px-4 py-2 text-gray-700 hover:text-gray-900 hover:bg-white/40 backdrop-blur-xl rounded-xl transition-all flex items-center gap-2">
              <Image className="w-4 h-4" />
              <span>Gallery</span>
            </a>
            <a href="#about" className="px-4 py-2 text-gray-700 hover:text-gray-900 hover:bg-white/40 backdrop-blur-xl rounded-xl transition-all flex items-center gap-2">
              <Info className="w-4 h-4" />
              <span>About</span>
            </a>
            <a href="#contact" className="px-4 py-2 text-gray-700 hover:text-gray-900 hover:bg-white/40 backdrop-blur-xl rounded-xl transition-all flex items-center gap-2">
              <Mail className="w-4 h-4" />
              <span>Contact</span>
            </a>
          </div>

          {/* User Profile */}
          <Button variant="ghost" size="icon" className="rounded-full hover:bg-white/40 backdrop-blur-xl">
            <User className="w-5 h-5" />
          </Button>
        </div>
      </div>
    </nav>
  );
}
