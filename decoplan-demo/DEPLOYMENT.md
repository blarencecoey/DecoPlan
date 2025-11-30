# DecoPlan Demo - Deployment Guide

## Build Process Overview

The DecoPlan demo is built using **Next.js 16** with the App Router. Here's how to compile and deploy it.

## Entry Points

### Main Application Files
- **`app/page.tsx`** - Main page component (root route `/`)
- **`app/layout.tsx`** - Root layout wrapper
- **`next.config.js`** - Build configuration
- **`package.json`** - Scripts and dependencies

### Build Output
- **`.next/`** - Compiled production build (created after `npm run build`)
- **`out/`** - Static export output (if using static export)

---

## Deployment Options

### Option 1: Vercel (Recommended - Easiest)

**Vercel** is created by the Next.js team and provides zero-config deployment.

#### Steps:

1. **Push to GitHub:**
   ```bash
   cd decoplan-demo
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/decoplan-demo.git
   git push -u origin main
   ```

2. **Deploy to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel auto-detects Next.js and deploys

3. **Custom Domain:**
   - In Vercel dashboard, go to Settings → Domains
   - Add your custom domain
   - Update DNS records as instructed

**Pros:**
- Zero configuration
- Automatic deployments on git push
- Built-in CDN and SSL
- Serverless functions support
- Free tier available

**Build Command:** `npm run build` (automatic)
**Output Directory:** `.next` (automatic)

---

### Option 2: Netlify

Similar to Vercel, with drag-and-drop support.

#### Steps:

1. **Build Configuration:**
   Create `netlify.toml`:
   ```toml
   [build]
     command = "npm run build"
     publish = ".next"

   [[plugins]]
     package = "@netlify/plugin-nextjs"
   ```

2. **Deploy:**
   - Connect GitHub repo at [netlify.com](https://netlify.com)
   - Or drag-and-drop build folder
   - Configure custom domain in Settings

**Pros:**
- Easy deployment
- Form handling and serverless functions
- Free SSL
- Continuous deployment

---

### Option 3: Static Export (GitHub Pages, S3, etc.)

For pure static hosting without server-side features.

#### Configuration:

1. **Update `next.config.js`:**
   ```javascript
   /** @type {import('next').NextConfig} */
   const nextConfig = {
     output: 'export',  // Enable static export
     reactStrictMode: true,
     transpilePackages: ['three'],
     images: {
       unoptimized: true,  // Required for static export
     },
   }

   module.exports = nextConfig
   ```

2. **Build:**
   ```bash
   npm run build
   ```

   This creates an `out/` folder with static HTML/CSS/JS.

3. **Deploy `out/` folder to:**
   - **GitHub Pages:**
     ```bash
     # Install gh-pages
     npm install -D gh-pages

     # Add to package.json scripts:
     "deploy": "next build && touch out/.nojekyll && gh-pages -d out -t true"

     # Deploy
     npm run deploy
     ```

   - **AWS S3:**
     ```bash
     aws s3 sync out/ s3://your-bucket-name --delete
     ```

   - **Cloudflare Pages:**
     - Connect repository
     - Build command: `npm run build`
     - Output directory: `out`

**Limitations:**
- No server-side rendering (SSR)
- No API routes
- No dynamic routing (unless pre-generated)
- Image optimization disabled

**Works for DecoPlan?** ✅ Yes! The demo is fully client-side.

---

### Option 4: Self-Hosted (Your Own Server)

For complete control with your own domain.

#### Requirements:
- Node.js 18+ installed on server
- Reverse proxy (Nginx/Apache)
- Process manager (PM2)

#### Steps:

1. **On Your Server:**
   ```bash
   # Clone or copy project to server
   cd /var/www/decoplan-demo

   # Install dependencies
   npm install

   # Build for production
   npm run build

   # Install PM2 (process manager)
   npm install -g pm2

   # Start with PM2
   pm2 start npm --name "decoplan" -- start
   pm2 save
   pm2 startup
   ```

2. **Configure Nginx:**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://localhost:3000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

3. **Enable HTTPS with Let's Encrypt:**
   ```bash
   sudo certbot --nginx -d yourdomain.com
   ```

4. **Restart services:**
   ```bash
   sudo systemctl restart nginx
   pm2 restart decoplan
   ```

**Pros:**
- Full control
- No third-party dependencies
- Custom server configurations
- Can run on your own domain

**Cons:**
- Requires server maintenance
- Manual updates
- Need to handle scaling

---

### Option 5: Docker Deployment

For containerized deployment on any platform.

#### Create `Dockerfile`:

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
ENV PORT 3000

CMD ["node", "server.js"]
```

#### Build and Run:
```bash
# Build image
docker build -t decoplan-demo .

# Run container
docker run -p 3000:3000 decoplan-demo

# Or with docker-compose
docker-compose up -d
```

---

## Build Commands Reference

```bash
# Development (hot reload)
npm run dev

# Production build
npm run build

# Start production server (after build)
npm start

# Lint code
npm run lint
```

---

## Environment Variables

If you need environment variables for your domain:

Create `.env.production`:
```env
NEXT_PUBLIC_SITE_URL=https://yourdomain.com
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

Access in code:
```typescript
const siteUrl = process.env.NEXT_PUBLIC_SITE_URL;
```

---

## Custom Domain Setup

### For Vercel/Netlify:
1. Add domain in dashboard
2. Update DNS:
   ```
   Type: CNAME
   Name: www (or @)
   Value: cname.vercel-dns.com (or netlify domain)
   ```

### For Self-Hosted:
1. Update DNS A record:
   ```
   Type: A
   Name: @
   Value: YOUR_SERVER_IP
   ```
2. Configure server (Nginx/Apache)
3. Enable SSL (Let's Encrypt)

---

## Performance Optimization

### Before Deployment:

1. **Analyze Bundle Size:**
   ```bash
   npm install -D @next/bundle-analyzer
   ```

   Update `next.config.js`:
   ```javascript
   const withBundleAnalyzer = require('@next/bundle-analyzer')({
     enabled: process.env.ANALYZE === 'true',
   })

   module.exports = withBundleAnalyzer(nextConfig)
   ```

   Run:
   ```bash
   ANALYZE=true npm run build
   ```

2. **Enable Compression:**
   Already handled by Next.js in production mode.

3. **Optimize Images:**
   Use Next.js Image component (already optimized).

---

## Recommended Deployment

**For Your Use Case:**

1. **Quick Demo/Personal Use:**
   - **Vercel** (free, instant, custom domain)

2. **Professional/Business:**
   - **Vercel Pro** or **Self-hosted** (more control)

3. **Static Only:**
   - **GitHub Pages** or **Cloudflare Pages** (free, simple)

4. **Enterprise:**
   - **Docker + Kubernetes** or **AWS ECS**

---

## Quick Start Deployment

### Fastest Way (Vercel):

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from project directory
cd decoplan-demo
vercel

# Follow prompts, done!
```

Your demo will be live at: `https://decoplan-demo.vercel.app`

Add custom domain: `vercel domains add yourdomain.com`

---

## Troubleshooting

### Build Fails:
```bash
# Clear cache and rebuild
rm -rf .next node_modules
npm install
npm run build
```

### Port Already in Use:
```bash
# Change port
PORT=3001 npm start
```

### Static Export Issues:
- Remove dynamic features (API routes)
- Disable image optimization
- Pre-render all routes

---

## Summary

**Entry Point for Compilation:**
- **Command:** `npm run build`
- **Config:** `next.config.js`
- **Output:** `.next/` folder (or `out/` for static export)

**Recommended Hosting:**
- **Easiest:** Vercel (zero-config, free)
- **Most Control:** Self-hosted VPS
- **Static:** GitHub Pages / Cloudflare Pages

**Custom Domain:** Configure in hosting provider dashboard + update DNS

Need help with a specific deployment method? Let me know!
