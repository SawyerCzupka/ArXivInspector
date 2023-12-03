"""
Script to use the arxiv_inspector library to load my arxiv pdfs into a Qdrant database.
"""

from llama_index.vector_stores import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models

import logging

from arxiv_inspector.indexing import ArxivIndexer
logging.basicConfig(level=logging.DEBUG)
# TEST_ID = '2309.17453'
TEST_ID = '2304.04613'
QDRANT_URL = "http://localhost:6333"
QDRANT_COLLECTION = "arxiv"

if __name__ == "__main__":
    client = QdrantClient(
        url=QDRANT_URL
    )

    client.recreate_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE)
    )

    vector_store = QdrantVectorStore(client=client, collection_name=QDRANT_COLLECTION)

    indexer = ArxivIndexer(vector_store=vector_store)

    # indexer.index_arxiv_pdf(pdf_path=f"../data/pdfs/{TEST_ID}.pdf")
    indexer.index_arxiv_directory(directory=f"../data/pdfs/")

# NEXT: Find out why this isn't adding nodes to the Qdrant database.
