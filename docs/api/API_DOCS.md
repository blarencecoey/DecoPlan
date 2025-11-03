# DecoPlan RAG API Documentation

Flask REST API for the DecoPlan furniture recommendation system using RAG (Retrieval-Augmented Generation).

## Getting Started

### Installation

1. Install dependencies:

**Option A: Minimal backend only (recommended for API)**
```bash
pip install -r requirements-backend.txt
```

**Option B: Full dependencies (includes training tools)**
```bash
pip install -r requirements.txt
```

### Running the Server

#### Basic Usage
```bash
python app.py
```

The server will start on `http://localhost:5000` by default.

#### Configuration via Environment Variables
```bash
export FLASK_HOST=0.0.0.0
export FLASK_PORT=8080
export FLASK_DEBUG=True
python app.py
```

Or inline:
```bash
FLASK_PORT=8080 python app.py
```

## API Endpoints

### 1. Health Check

Check if the server and RAG system are ready.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "ready": true,
  "database_path": "./furniture_db"
}
```

**Example:**
```bash
curl http://localhost:5000/health
```

---

### 2. Search Furniture

Perform semantic search for furniture items with optional filtering.

**Endpoint:** `POST /api/search`

**Request Body:**
```json
{
  "query": "modern sofa",
  "n_results": 10,
  "filters": {
    "Style": "Modern",
    "Room_Type": "Living Room",
    "Is_Accessory": false
  }
}
```

**Parameters:**
- `query` (string, required): Search query describing the furniture
- `n_results` (integer, optional): Number of results to return (default: 15)
- `filters` (object, optional): Filter criteria:
  - `Style`: e.g., "Modern", "Traditional", "Minimalist"
  - `Room_Type`: e.g., "Living Room", "Bedroom", "Kitchen"
  - `Furniture_Type`: e.g., "Sofa", "Table", "Chair"
  - `Is_Accessory`: boolean (true/false)

**Response:**
```json
{
  "success": true,
  "query": "modern sofa",
  "n_results": 10,
  "results": [
    {
      "id": "FURN-12345",
      "Name": "Modern Sectional Sofa",
      "Style": "Modern",
      "Room_Type": "Living Room",
      "Furniture_Type": "Sofa",
      "Material": "Fabric",
      "Color": "Gray",
      "Price": 1299.99,
      "Dimensions": "84x36x34",
      "Is_Accessory": false,
      "distance": 0.234
    }
  ]
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "modern minimalist sofa",
    "n_results": 5,
    "filters": {
      "Style": "Modern",
      "Room_Type": "Living Room"
    }
  }'
```

---

### 3. Enhance Prompt (RAG)

Enhance a user prompt with relevant furniture context for use with LLMs.

**Endpoint:** `POST /api/enhance-prompt`

**Request Body:**
```json
{
  "prompt": "I want a modern living room",
  "room_type": "Living Room",
  "style": "Modern",
  "n_items": 15
}
```

**Parameters:**
- `prompt` (string, required): User's original prompt
- `room_type` (string, optional): Filter by room type
- `style` (string, optional): Filter by style
- `n_items` (integer, optional): Number of furniture items to include in context (default: 15)

**Response:**
```json
{
  "success": true,
  "original_prompt": "I want a modern living room",
  "enhanced_prompt": "Based on the following furniture options:\n\n1. Modern Sectional Sofa...\n\nUser request: I want a modern living room",
  "room_type": "Living Room",
  "style": "Modern"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/enhance-prompt \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Design a cozy minimalist bedroom",
    "room_type": "Bedroom",
    "style": "Minimalist",
    "n_items": 10
  }'
```

---

### 4. Database Statistics

Get statistics about the furniture database.

**Endpoint:** `GET /api/stats`

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_items": 10108,
    "styles": ["Modern", "Traditional", "Minimalist", "Industrial", "Scandinavian"],
    "room_types": ["Living Room", "Bedroom", "Dining Room", "Kitchen", "Office"],
    "furniture_types": ["Sofa", "Table", "Chair", "Bed", "Desk"]
  }
}
```

**Example:**
```bash
curl http://localhost:5000/api/stats
```

---

### 5. Available Filters

Get all available filter values for searches.

**Endpoint:** `GET /api/filters`

**Response:**
```json
{
  "success": true,
  "filters": {
    "styles": ["Modern", "Traditional", "Minimalist", "Industrial", "Scandinavian"],
    "room_types": ["Living Room", "Bedroom", "Dining Room", "Kitchen", "Office"],
    "furniture_types": ["Sofa", "Table", "Chair", "Bed", "Desk"]
  }
}
```

**Example:**
```bash
curl http://localhost:5000/api/filters
```

---

### 6. Batch Search

Perform multiple searches in a single request for efficiency.

**Endpoint:** `POST /api/batch-search`

**Request Body:**
```json
{
  "queries": [
    {
      "query": "modern sofa",
      "n_results": 5
    },
    {
      "query": "wooden dining table",
      "n_results": 10,
      "filters": {
        "Room_Type": "Dining Room"
      }
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "batch_results": [
    {
      "success": true,
      "query": "modern sofa",
      "results": [...]
    },
    {
      "success": true,
      "query": "wooden dining table",
      "results": [...]
    }
  ]
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/batch-search \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      {"query": "modern sofa", "n_results": 3},
      {"query": "wooden table", "n_results": 3}
    ]
  }'
```

---

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (missing required fields, invalid parameters)
- `404`: Endpoint not found
- `500`: Internal server error
- `503`: Service unavailable (RAG system not initialized)

**Error Response Format:**
```json
{
  "error": "Description of the error"
}
```

---

## Python Client Example

```python
import requests

# Base URL
BASE_URL = "http://localhost:5000"

# Search for furniture
def search_furniture(query, n_results=10, filters=None):
    response = requests.post(
        f"{BASE_URL}/api/search",
        json={
            "query": query,
            "n_results": n_results,
            "filters": filters or {}
        }
    )
    return response.json()

# Enhance prompt with RAG
def enhance_prompt(prompt, room_type=None, style=None):
    response = requests.post(
        f"{BASE_URL}/api/enhance-prompt",
        json={
            "prompt": prompt,
            "room_type": room_type,
            "style": style
        }
    )
    return response.json()

# Example usage
if __name__ == "__main__":
    # Search for modern sofas
    results = search_furniture(
        query="modern minimalist sofa",
        n_results=5,
        filters={"Style": "Modern", "Room_Type": "Living Room"}
    )
    print(f"Found {results['n_results']} items")

    # Enhance a prompt
    enhanced = enhance_prompt(
        prompt="I want a cozy bedroom",
        room_type="Bedroom",
        style="Scandinavian"
    )
    print("Enhanced prompt:", enhanced['enhanced_prompt'][:100])
```

---

## JavaScript/Frontend Example

```javascript
// Search for furniture
async function searchFurniture(query, nResults = 10, filters = {}) {
  const response = await fetch('http://localhost:5000/api/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query: query,
      n_results: nResults,
      filters: filters
    })
  });

  return await response.json();
}

// Enhance prompt with RAG
async function enhancePrompt(prompt, roomType = null, style = null) {
  const response = await fetch('http://localhost:5000/api/enhance-prompt', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      prompt: prompt,
      room_type: roomType,
      style: style
    })
  });

  return await response.json();
}

// Example usage
(async () => {
  // Search
  const results = await searchFurniture(
    "modern sofa",
    5,
    { Style: "Modern", Room_Type: "Living Room" }
  );
  console.log('Search results:', results);

  // Enhance prompt
  const enhanced = await enhancePrompt(
    "Design a cozy bedroom",
    "Bedroom",
    "Scandinavian"
  );
  console.log('Enhanced prompt:', enhanced.enhanced_prompt);
})();
```

---

## Performance Considerations

- **First Request Latency**: Initial requests may take 2-3 seconds as the embedding model loads
- **Subsequent Requests**: ~100-500ms depending on query complexity
- **Batch Searches**: More efficient than multiple single searches
- **Database Size**: 10,108 items (~40MB ChromaDB)
- **Embedding Model**: all-MiniLM-L6-v2 (lightweight, ~80MB)

---

## Deployment

### Production Deployment

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t decoplan-rag .
docker run -p 5000:5000 decoplan-rag
```

---

## Troubleshooting

### Database Not Found
```
Error: Database not found at ./furniture_db
```
**Solution:** Ensure the `furniture_db` directory exists and contains the ChromaDB files. Run `rag/build_furniture_db.py` if needed.

### Model Loading Issues
```
Error: Failed to load embedding model
```
**Solution:** The first run downloads the embedding model (~80MB). Ensure internet connection and sufficient disk space.

### CORS Errors
CORS is enabled by default for all origins. If you need to restrict origins, modify the CORS configuration in `app.py`:
```python
CORS(app, resources={r"/api/*": {"origins": "https://yourdomain.com"}})
```

---

## License

See the main project LICENSE file.
