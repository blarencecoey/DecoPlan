#!/usr/bin/env python3
"""
Convenience script to run the Flask backend from project root.
This handles Python path setup automatically.
"""

import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Now import and run the app
from api.app import app, initialize_rag_components, logger
import os

if __name__ == '__main__':
    logger.info("Starting DecoPlan RAG Flask Backend")

    if not initialize_rag_components():
        logger.error("Failed to initialize RAG components. Server will start but endpoints will be unavailable.")

    # Get configuration from environment variables
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    logger.info(f"Starting server on {host}:{port} (debug={debug})")
    app.run(host=host, port=port, debug=debug)
