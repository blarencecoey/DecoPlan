"""
Flask Backend for DecoPlan RAG Model
Provides REST API endpoints for furniture retrieval and RAG-enhanced prompts
"""

# Fix SQLite version for ChromaDB (must be FIRST, before any other imports)
try:
    __import__("pysqlite3")
    import sys

    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass  # pysqlite3 not installed, will use system sqlite3

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
import logging

# Add backend directory to path for imports (must be before RAG imports)
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Import RAG components
from rag.furniture_retriever import FurnitureRetriever
from rag.rag_inference import RAGInference

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Global variables for RAG components
retriever = None
rag_inference = None
# Update path to point to data/furniture_db
DB_PATH = str(Path(__file__).parent.parent.parent / "data" / "furniture_db")


def initialize_rag_components():
    """Initialize RAG components on startup"""
    global retriever, rag_inference

    try:
        logger.info(f"Initializing RAG components with database at {DB_PATH}")

        # Check if database exists
        if not os.path.exists(DB_PATH):
            raise FileNotFoundError(f"Database not found at {DB_PATH}")

        # Initialize retriever and RAG inference
        retriever = FurnitureRetriever(db_path=DB_PATH)
        rag_inference = RAGInference(db_path=DB_PATH)

        logger.info("RAG components initialized successfully")
        return True

    except Exception as e:
        logger.error(f"Failed to initialize RAG components: {str(e)}")
        return False


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    is_ready = retriever is not None and rag_inference is not None

    return jsonify(
        {
            "status": "healthy" if is_ready else "initializing",
            "ready": is_ready,
            "database_path": DB_PATH,
        }
    ), (200 if is_ready else 503)


@app.route("/api/search", methods=["POST"])
def search_furniture():
    """
    Search for furniture items using semantic search

    Request body:
    {
        "query": "modern sofa",
        "n_results": 10,
        "filters": {
            "Style": "Modern",
            "Room_Type": "Living Room",
            "Is_Accessory": false
        }
    }
    """
    if retriever is None:
        return jsonify({"error": "RAG system not initialized"}), 503

    try:
        data = request.get_json()

        # Validate required fields
        if "query" not in data:
            return jsonify({"error": "Missing required field: query"}), 400

        query = data["query"]
        n_results = data.get("n_results", 15)
        filters = data.get("filters", {})

        # Perform retrieval
        results = retriever.retrieve(query=query, n_results=n_results, filters=filters)

        return (
            jsonify(
                {
                    "success": True,
                    "query": query,
                    "n_results": len(results),
                    "results": results,
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Error in search_furniture: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/recommendations", methods=["POST"])
def get_recommendations():
    """
    Get furniture recommendations based on user prompt (for frontend integration)

    Request body:
    {
        "prompt": "I want a cozy minimalist bedroom",
        "furniture_types": ["Sofa", "Chair", "Table"]  # optional
    }

    Response format matches frontend RAGResponse interface
    """
    if retriever is None:
        return jsonify({"error": "RAG system not initialized"}), 503

    try:
        import time

        start_time = time.time()

        data = request.get_json()

        # Validate required fields
        if "prompt" not in data:
            return jsonify({"error": "Missing required field: prompt"}), 400

        prompt = data["prompt"]
        n_results_requested = data.get("n_results", 15)
        filters = data.get("filters", {})

        # Handle furniture_types filtering
        furniture_types = data.get("furniture_types", [])
        logger.info(f"Received furniture_types: {furniture_types}")

        # Mapping of general types to specific patterns in the database
        type_patterns = {
            "Bed": [
                "Bed",
                "Bed frame",
                "Day-bed",
                "Bunk bed",
                "Loft bed",
                "Divan bed",
                "Ottoman bed",
                "Stackable bed",
                "Upholstered bed",
                "Four-poster bed",
                "Reversible bed",
                "Extendable bed",
                "Ext bed",
            ],
            "Wardrobe": ["Wardrobe"],
            "Table": ["Table"],
            "Dining Table": ["Dining Table"],
            "Coffee Table": ["Coffee Table"],
            "Desk": ["Desk"],
            "Chair": ["Chair"],
            "Armchair": ["Armchair"],
            "Sofa": ["Sofa"],
            "Bench": ["Bench"],
            "Stool": ["Stool"],
            "Bookshelf": ["Bookshelf", "Bookcase"],
            "Dresser": ["Dresser"],
            "Cabinet": ["Cabinet"],
            "Nightstand": ["Nightstand"],
            "Recliner": ["Recliner"],
        }

        # If furniture types are specified, retrieve more results and filter in Python
        if furniture_types and len(furniture_types) > 0:
            # Get all matching patterns for selected types
            matching_patterns = []
            for ftype in furniture_types:
                if ftype in type_patterns:
                    matching_patterns.extend(type_patterns[ftype])

            logger.info(f"Matching patterns: {matching_patterns}")

            # Retrieve more results to ensure we get enough after filtering
            all_results = retriever.retrieve(
                query=prompt,
                n_results=n_results_requested * 3,  # Get 3x more to filter
                filters=filters if filters else None,
            )

            # Filter results based on patterns
            results = []
            for item in all_results:
                item_type = item.get("furniture_type", "")
                # Check if item's furniture_type starts with any of the matching patterns
                if any(item_type.startswith(pattern) for pattern in matching_patterns):
                    results.append(item)
                    if len(results) >= n_results_requested:
                        break

            logger.info(
                f"Filtered to {len(results)} results from {len(all_results)} total"
            )
        else:
            # No filtering, retrieve normally
            results = retriever.retrieve(
                query=prompt,
                n_results=n_results_requested,
                filters=filters if filters else None,
            )
            logger.info(f"Retrieved {len(results)} results without filtering")

        # Transform results to match frontend FurnitureItem interface
        recommendations = []
        for item in results:
            furniture_item = {
                "id": item["id"],
                "name": item["name"],
                "category": item["furniture_type"],
                "style": item["feel"],
                "price": 0.0,  # Placeholder - price not in database
                "description": item["description"],
                "imageUrl": f"https://images.unsplash.com/photo-{hash(item['id']) % 1000000000}?w=400",  # Placeholder
                "dimensions": item.get("dimensions", "N/A"),
                "material": item.get("material", "N/A"),
                "color": item.get("color", "N/A"),
                "relevanceScore": item.get("relevance_score", 0.0),
            }
            recommendations.append(furniture_item)

        processing_time = time.time() - start_time

        # Return in RAGResponse format
        return (
            jsonify(
                {
                    "query": prompt,
                    "recommendations": recommendations,
                    "totalResults": len(recommendations),
                    "processingTime": round(processing_time, 3),
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Error in get_recommendations: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/enhance-prompt", methods=["POST"])
def enhance_prompt():
    """
    Enhance a user prompt with relevant furniture context using RAG

    Request body:
    {
        "prompt": "I want a modern living room",
        "room_type": "Living Room",
        "style": "Modern",
        "n_items": 15
    }
    """
    if rag_inference is None:
        return jsonify({"error": "RAG system not initialized"}), 503

    try:
        data = request.get_json()

        # Validate required fields
        if "prompt" not in data:
            return jsonify({"error": "Missing required field: prompt"}), 400

        user_prompt = data["prompt"]
        room_type = data.get("room_type", None)
        style = data.get("style", None)
        n_items = data.get("n_items", 15)

        # Create enhanced prompt
        enhanced_prompt = rag_inference.create_prompt_with_context(
            user_prompt=user_prompt, room_type=room_type, style=style, n_items=n_items
        )

        return (
            jsonify(
                {
                    "success": True,
                    "original_prompt": user_prompt,
                    "enhanced_prompt": enhanced_prompt,
                    "room_type": room_type,
                    "style": style,
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Error in enhance_prompt: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/stats", methods=["GET"])
def get_database_stats():
    """Get statistics about the furniture database"""
    if retriever is None:
        return jsonify({"error": "RAG system not initialized"}), 503

    try:
        stats = retriever.get_stats()
        return jsonify({"success": True, "stats": stats}), 200

    except Exception as e:
        logger.error(f"Error in get_database_stats: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/filters", methods=["GET"])
def get_available_filters():
    """Get available filter values (styles, room types, furniture types)"""
    if retriever is None:
        return jsonify({"error": "RAG system not initialized"}), 503

    try:
        stats = retriever.get_stats()

        return (
            jsonify(
                {
                    "success": True,
                    "filters": {
                        "styles": stats.get("styles", []),
                        "room_types": stats.get("room_types", []),
                        "furniture_types": stats.get("furniture_types", []),
                    },
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Error in get_available_filters: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/batch-search", methods=["POST"])
def batch_search():
    """
    Perform multiple searches in a single request

    Request body:
    {
        "queries": [
            {"query": "modern sofa", "n_results": 5},
            {"query": "wooden table", "n_results": 10}
        ]
    }
    """
    if retriever is None:
        return jsonify({"error": "RAG system not initialized"}), 503

    try:
        data = request.get_json()

        if "queries" not in data or not isinstance(data["queries"], list):
            return jsonify({"error": "Missing or invalid 'queries' field"}), 400

        results = []
        for query_item in data["queries"]:
            if "query" not in query_item:
                results.append({"error": "Missing query field"})
                continue

            try:
                query_results = retriever.retrieve(
                    query=query_item["query"],
                    n_results=query_item.get("n_results", 15),
                    filters=query_item.get("filters", {}),
                )
                results.append(
                    {
                        "success": True,
                        "query": query_item["query"],
                        "results": query_results,
                    }
                )
            except Exception as e:
                results.append(
                    {"success": False, "query": query_item["query"], "error": str(e)}
                )

        return jsonify({"success": True, "batch_results": results}), 200

    except Exception as e:
        logger.error(f"Error in batch_search: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    # Initialize RAG components before starting server
    logger.info("Starting DecoPlan RAG Flask Backend")

    if not initialize_rag_components():
        logger.error(
            "Failed to initialize RAG components. Server will start but endpoints will be unavailable."
        )

    # Get configuration from environment variables
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    logger.info(f"Starting server on {host}:{port} (debug={debug})")
    app.run(host=host, port=port, debug=debug)
