# Flask Backend Integration Guide

This frontend is designed to work with your Flask backend RAG model. Follow these steps to connect it to your existing implementation.

## Backend API Endpoint

The frontend expects your Flask backend to expose the following endpoint:

### POST `/api/recommendations`

**Request Body:**
```json
{
  "prompt": "I want a cozy japanese living room"
}
```

**Response Format:**
```json
{
  "query": "I want a cozy japanese living room",
  "recommendations": [
    {
      "id": "unique-id",
      "name": "Furniture Item Name",
      "category": "Seating|Tables|Lighting|Storage|Decor",
      "style": "Japanese|Modern|Scandinavian|etc",
      "price": 89.99,
      "description": "Item description",
      "imageUrl": "https://...",
      "dimensions": "24\" x 24\" x 4\"",
      "material": "Cotton, Memory Foam",
      "color": "Natural Beige",
      "relevanceScore": 0.95
    }
  ],
  "totalResults": 6,
  "processingTime": 1.2
}
```

## Configuration Steps

1. **Set Your Flask Backend URL**

   Create a `.env` file in the root directory:
   ```
   NEXT_PUBLIC_FLASK_API_URL=http://localhost:5000
   ```

2. **Update the API Service**

   Open `/services/api.ts` and uncomment the actual fetch call (lines 14-27):
   ```typescript
   const response = await fetch(`${FLASK_API_URL}/api/recommendations`, {
     method: 'POST',
     headers: {
       'Content-Type': 'application/json',
     },
     body: JSON.stringify({ prompt }),
   });
   
   if (!response.ok) {
     throw new Error('Failed to fetch recommendations');
   }
   
   return await response.json();
   ```

3. **Remove Mock Function**

   Delete or comment out the `mockFlaskResponse` function (lines 30-120 in `/services/api.ts`)

4. **Enable CORS on Flask Backend**

   Ensure your Flask app allows CORS requests:
   ```python
   from flask import Flask
   from flask_cors import CORS

   app = Flask(__name__)
   CORS(app)  # Enable CORS for all routes
   ```

## Example Flask Implementation

Here's a basic example of what your Flask endpoint might look like:

```python
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    # Your RAG model logic here
    recommendations = your_rag_model.query(prompt)
    
    return jsonify({
        'query': prompt,
        'recommendations': recommendations,
        'totalResults': len(recommendations),
        'processingTime': processing_time
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## Testing

1. Start your Flask backend on port 5000
2. The frontend will automatically connect to it
3. Try searching with prompts like "I want a cozy japanese living room"

## Troubleshooting

- **CORS Errors**: Make sure CORS is enabled on your Flask backend
- **Connection Refused**: Verify your Flask server is running on the correct port
- **404 Errors**: Check that your endpoint matches `/api/recommendations`
- **Data Format**: Ensure your response matches the expected TypeScript interface in `/types/furniture.ts`
