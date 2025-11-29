#!/usr/bin/env python3
"""
Build vector database from furniture catalog for RAG retrieval.
"""

# Fix SQLite version for ChromaDB (must be before any chromadb imports)
try:
    __import__("pysqlite3")
    import sys

    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass  # pysqlite3 not installed, will use system sqlite3

import pandas as pd
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from pathlib import Path
import argparse
from tqdm import tqdm
import json


class FurnitureVectorDB:
    """Build and manage vector database for furniture catalog."""

    def __init__(
        self, db_path: str = "./furniture_db", model_name: str = "all-MiniLM-L6-v2"
    ):
        """
        Initialize the vector database builder.

        Args:
            db_path: Path to store the ChromaDB database
            model_name: Name of the sentence transformer model to use for embeddings
        """
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)

        print(f"Loading embedding model: {model_name}")
        self.embedding_model = SentenceTransformer(model_name)

        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(self.db_path), settings=Settings(anonymized_telemetry=False)
        )

    def create_furniture_description(self, row: pd.Series) -> str:
        """
        Create a rich text description of furniture for embedding.

        Args:
            row: Pandas series containing furniture data

        Returns:
            Formatted description string
        """
        description = (
            f"{row['Name']}: A {row['Feel']} style {row['Furniture Type']} "
            f"made of {row['Material']} in {row['Color']} color. "
            f"Dimensions: {row['Dimensions (cm)']}."
        )
        return description

    def build_database(
        self, furniture_csv_path: str, collection_name: str = "furniture_catalog"
    ):
        """
        Build the vector database from furniture CSV.

        Args:
            furniture_csv_path: Path to the furniture CSV file
            collection_name: Name of the ChromaDB collection
        """
        print(f"Loading furniture data from: {furniture_csv_path}")
        df = pd.read_csv(furniture_csv_path)
        print(f"Loaded {len(df)} furniture items")

        # Create or get collection
        try:
            self.client.delete_collection(collection_name)
            print(f"Deleted existing collection: {collection_name}")
        except:
            pass

        collection = self.client.create_collection(
            name=collection_name, metadata={"hnsw:space": "cosine"}
        )
        print(f"Created collection: {collection_name}")

        # Create descriptions and embeddings
        descriptions = []
        metadatas = []
        ids = []

        print("Creating furniture descriptions...")
        for idx, row in tqdm(df.iterrows(), total=len(df)):
            description = self.create_furniture_description(row)
            descriptions.append(description)

            # Store metadata
            metadatas.append(
                {
                    "name": row["Name"],
                    "furniture_type": row["Furniture Type"],
                    "material": row["Material"],
                    "color": row["Color"],
                    "feel": row["Feel"],
                    "is_accessory": str(row["Is_Accessory"]),
                    "dimensions": row["Dimensions (cm)"],
                }
            )

            ids.append(f"furniture_{idx}")

        # Generate embeddings in batches
        print("Generating embeddings...")
        batch_size = 100
        for i in tqdm(range(0, len(descriptions), batch_size)):
            batch_descriptions = descriptions[i : i + batch_size]
            batch_metadatas = metadatas[i : i + batch_size]
            batch_ids = ids[i : i + batch_size]

            # Generate embeddings
            embeddings = self.embedding_model.encode(
                batch_descriptions, show_progress_bar=False
            ).tolist()

            # Add to collection
            collection.add(
                documents=batch_descriptions,
                embeddings=embeddings,
                metadatas=batch_metadatas,
                ids=batch_ids,
            )

        print(f"✓ Successfully built vector database with {len(descriptions)} items")
        print(f"  Database location: {self.db_path}")

        # Save statistics
        stats = {
            "total_items": len(descriptions),
            "furniture_types": df["Furniture Type"].value_counts().to_dict(),
            "materials": df["Material"].value_counts().to_dict(),
            "feels": df["Feel"].value_counts().to_dict(),
        }

        stats_path = self.db_path / "stats.json"
        with open(stats_path, "w") as f:
            json.dump(stats, f, indent=2)
        print(f"  Statistics saved to: {stats_path}")

        return collection


def main():
    parser = argparse.ArgumentParser(
        description="Build furniture vector database for RAG"
    )
    # Default paths relative to project root
    project_root = Path(__file__).parent.parent.parent
    default_csv = str(
        project_root
        / "data"
        / "datasets"
        / "Input"
        / "Furniture Dataset - Furniture Data.csv"
    )
    default_db = str(project_root / "data" / "furniture_db")

    parser.add_argument(
        "--furniture_csv",
        type=str,
        default=default_csv,
        help="Path to furniture CSV file",
    )
    parser.add_argument(
        "--db_path",
        type=str,
        default=default_db,
        help="Path to store the vector database",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="all-MiniLM-L6-v2",
        help="Sentence transformer model name",
    )
    parser.add_argument(
        "--collection_name",
        type=str,
        default="furniture_catalog",
        help="ChromaDB collection name",
    )

    args = parser.parse_args()

    # Build database
    db_builder = FurnitureVectorDB(db_path=args.db_path, model_name=args.model)
    db_builder.build_database(args.furniture_csv, args.collection_name)


if __name__ == "__main__":
    main()
