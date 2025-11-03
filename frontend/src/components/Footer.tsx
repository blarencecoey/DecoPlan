import { Facebook, Instagram, Twitter, Mail, Sparkles } from 'lucide-react';

export function Footer() {
  return (
    <footer className="border-t border-white/20 bg-white/10 backdrop-blur-3xl mt-20">
      <div className="container mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-br from-[#D4735E] to-[#C96A54] rounded-lg flex items-center justify-center">
                <span className="text-white">D</span>
              </div>
              <span className="text-xl text-gray-800">Homemah</span>
            </div>
            <p className="text-sm text-gray-600">
              Transform your HDB into your dream home with AI-powered interior design recommendations.
            </p>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h4 className="text-gray-900">Quick Links</h4>
            <ul className="space-y-2 text-sm text-gray-600">
              <li><a href="#home" className="hover:text-[#D4735E] transition-colors">Home</a></li>
              <li><a href="#gallery" className="hover:text-[#D4735E] transition-colors">Gallery</a></li>
              <li><a href="#about" className="hover:text-[#D4735E] transition-colors">About Us</a></li>
              <li><a href="#contact" className="hover:text-[#D4735E] transition-colors">Contact</a></li>
            </ul>
          </div>

          {/* Resources */}
          <div className="space-y-4">
            <h4 className="text-gray-900">Resources</h4>
            <ul className="space-y-2 text-sm text-gray-600">
              <li><a href="#" className="hover:text-[#D4735E] transition-colors">Design Guide</a></li>
              <li><a href="#" className="hover:text-[#D4735E] transition-colors">HDB Tips</a></li>
              <li><a href="#" className="hover:text-[#D4735E] transition-colors">Blog</a></li>
              <li><a href="#" className="hover:text-[#D4735E] transition-colors">FAQ</a></li>
            </ul>
          </div>

          {/* Connect */}
          <div className="space-y-4">
            <h4 className="text-gray-900">Connect</h4>
            <div className="flex gap-3">
              <a
                href="#"
                className="w-10 h-10 bg-white/20 backdrop-blur-xl border border-white/30 rounded-full flex items-center justify-center hover:bg-white/40 hover:border-white/50 transition-all"
              >
                <Facebook className="w-5 h-5" />
              </a>
              <a
                href="#"
                className="w-10 h-10 bg-white/20 backdrop-blur-xl border border-white/30 rounded-full flex items-center justify-center hover:bg-white/40 hover:border-white/50 transition-all"
              >
                <Instagram className="w-5 h-5" />
              </a>
              <a
                href="#"
                className="w-10 h-10 bg-white/20 backdrop-blur-xl border border-white/30 rounded-full flex items-center justify-center hover:bg-white/40 hover:border-white/50 transition-all"
              >
                <Twitter className="w-5 h-5" />
              </a>
              <a
                href="#"
                className="w-10 h-10 bg-white/20 backdrop-blur-xl border border-white/30 rounded-full flex items-center justify-center hover:bg-white/40 hover:border-white/50 transition-all"
              >
                <Mail className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-white/20 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-gray-600">
            © 2025 Homemah. All rights reserved.
          </p>
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <Sparkles className="w-4 h-4 text-[#D4735E]" />
            <span>Powered by AI & RAG Technology</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
