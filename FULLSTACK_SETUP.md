# DecoPlan Full Stack Setup Guide

Complete guide to running the Flask backend and React frontend together.

## Overview

- **Backend:** Flask REST API with RAG furniture recommendations
- **Frontend:** React + TypeScript + Vite UI
- **Communication:** REST API over HTTP with CORS enabled

---

## Quick Start

### Terminal 1: Start Backend

```bash
# Setup backend (first time only)
./setup_backend.sh

# Start Flask server
./start_backend.sh
```

Server runs at: `http://localhost:5000`

### Terminal 2: Start Frontend

```bash
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

Frontend runs at: `http://localhost:3000`

---

## Detailed Setup Instructions

### 1. Backend Setup

#### First-Time Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install minimal backend dependencies
pip install -r requirements-backend.txt
```

#### Start Backend

```bash
# Activate venv
source venv/bin/activate

# Run Flask app
python app.py
```

**Expected output:**
```
Starting DecoPlan RAG Flask Backend
Initializing RAG components with database at ./furniture_db
Loading embedding model: all-MiniLM-L6-v2
RAG components initialized successfully
Starting server on 0.0.0.0:5000
```

#### Test Backend

```bash
# Health check
curl http://localhost:5000/health

# Test recommendations endpoint
curl -X POST http://localhost:5000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "modern minimalist living room"}'
```

---

### 2. Frontend Setup

#### First-Time Setup

```bash
cd frontend

# Install dependencies
npm install
```

#### Configure Environment (Optional)

The frontend is pre-configured to connect to `http://localhost:5000`. To change the backend URL:

1. Copy `.env.example` to `.env.development`:
   ```bash
   cp .env.example .env.development
   ```

2. Edit `.env.development`:
   ```bash
   VITE_FLASK_API_URL=http://localhost:5000
   ```

#### Start Frontend

```bash
npm run dev
```

**Expected output:**
```
VITE v6.3.5  ready in 500 ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
```

The browser will automatically open to `http://localhost:3000`

---

## How It Works

### Data Flow

```
User Input (Frontend)
    ↓
    POST /api/recommendations
    { "prompt": "modern sofa" }
    ↓
Flask Backend
    ↓
RAG System (ChromaDB + sentence-transformers)
    ↓
Semantic Search → Top 15 furniture items
    ↓
Response (Frontend)
    {
      "query": "modern sofa",
      "recommendations": [...],
      "totalResults": 15,
      "processingTime": 0.234
    }
    ↓
Display Results
```

### API Integration

**Frontend:** `frontend/src/services/api.ts`
```typescript
const FLASK_API_URL = import.meta.env.VITE_FLASK_API_URL || 'http://localhost:5000';

export async function getFurnitureRecommendations(prompt: string) {
  const response = await fetch(`${FLASK_API_URL}/api/recommendations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt })
  });
  return await response.json();
}
```

**Backend:** `app.py`
```python
@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    prompt = request.json['prompt']
    results = retriever.retrieve(query=prompt, n_results=15)
    # Transform to frontend format
    return jsonify({
        "query": prompt,
        "recommendations": [...],
        "totalResults": len(results)
    })
```

---

## Available API Endpoints

### Frontend Integration Endpoint

- **POST /api/recommendations** - Get furniture recommendations
  ```json
  Request: { "prompt": "cozy bedroom" }
  Response: { "query", "recommendations", "totalResults", "processingTime" }
  ```

### Additional Backend Endpoints

- **GET /health** - Check backend status
- **POST /api/search** - Advanced search with filters
- **POST /api/enhance-prompt** - RAG-enhanced prompts
- **GET /api/stats** - Database statistics
- **GET /api/filters** - Available filter options
- **POST /api/batch-search** - Multiple searches

See `API_DOCS.md` for complete API documentation.

---

## Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError: No module named 'flask'`
```bash
# Solution: Activate venv and install dependencies
source venv/bin/activate
pip install -r requirements-backend.txt
```

**Problem:** `Database not found at ./furniture_db`
```bash
# Solution: Build the database first
cd rag
python build_furniture_db.py
```

**Problem:** `ImportError: cannot import name 'escape' from 'jinja2'`
```bash
# Solution: Use virtual environment (not system Python)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-backend.txt
```

### Frontend Issues

**Problem:** `Failed to fetch recommendations`
```bash
# Check:
1. Is backend running? curl http://localhost:5000/health
2. Is CORS enabled? (Should be by default)
3. Check browser console for detailed error
```

**Problem:** `npm: command not found`
```bash
# Solution: Install Node.js
# Ubuntu/Debian:
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Problem:** CORS errors in browser console
```bash
# Backend CORS is already enabled
# If still having issues, check Flask logs for errors
```

### Network Issues

**Problem:** Frontend can't connect to backend
```bash
# Verify backend is accessible:
curl http://localhost:5000/health

# Check ports:
# Backend: 5000 (Flask)
# Frontend: 3000 (Vite)
```

---

## Production Deployment

### Backend (Flask)

Use Gunicorn for production:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Or with Docker:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements-backend.txt .
RUN pip install -r requirements-backend.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Frontend (React)

Build for production:

```bash
cd frontend
npm run build
```

Serve with nginx, Vercel, Netlify, etc.

**Update environment variable for production:**
```bash
VITE_FLASK_API_URL=https://your-backend-api.com
```

---

## Project Structure

```
DecoPlan LLM/
├── app.py                     # Flask backend
├── requirements-backend.txt   # Backend dependencies
├── setup_backend.sh          # Backend setup script
├── start_backend.sh          # Backend start script
├── API_DOCS.md               # API documentation
├── FULLSTACK_SETUP.md        # This file
├── rag/                      # RAG implementation
│   ├── furniture_retriever.py
│   ├── rag_inference.py
│   └── build_furniture_db.py
├── furniture_db/             # ChromaDB vector database
└── frontend/                 # React frontend
    ├── src/
    │   ├── App.tsx
    │   ├── components/
    │   ├── services/
    │   │   └── api.ts        # Backend integration
    │   └── types/
    │       └── furniture.ts  # TypeScript interfaces
    ├── .env.development      # Dev environment config
    ├── .env.example          # Example config
    ├── package.json
    └── vite.config.ts
```

---

## Development Workflow

1. **Start Backend** (Terminal 1)
   ```bash
   source venv/bin/activate
   python app.py
   ```

2. **Start Frontend** (Terminal 2)
   ```bash
   cd frontend
   npm run dev
   ```

3. **Make Changes**
   - Backend: Edit Python files, Flask auto-reloads in debug mode
   - Frontend: Edit React files, Vite hot-reloads automatically

4. **Test Integration**
   - Use browser DevTools Network tab to inspect API calls
   - Check Flask terminal for backend logs
   - Use Postman/curl to test endpoints directly

---

## Performance Notes

- **First Request:** 2-3 seconds (embedding model loads)
- **Subsequent Requests:** 100-500ms
- **Database Size:** 10,108 furniture items (~40MB)
- **Frontend Build:** ~1-2MB gzipped

---

## Next Steps

### Enhancements

1. **Add Real Images**
   - Current: Placeholder URLs
   - Solution: Add `imageUrl` column to furniture database

2. **Add Real Prices**
   - Current: Placeholder price of 0.0
   - Solution: Add `price` column to furniture database

3. **Filter Integration**
   - Current: Frontend has filter UI but not connected
   - Solution: Pass filters from FilterPanel to API

4. **Pagination**
   - Current: Shows all results at once
   - Solution: Implement "Load More" functionality

5. **Authentication**
   - Add user accounts
   - Save search history
   - Personalized recommendations

---

## Support

- **API Documentation:** See `API_DOCS.md`
- **Frontend Guidelines:** See `frontend/src/guidelines/Guidelines.md`
- **Issues:** Check browser console and Flask logs for errors

---

## License

See main project LICENSE file.
