"""
Script to use the arxiv_inspector library to load my arxiv pdfs into a Qdrant database.
"""
import os
import re

from llama_index.vector_stores import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List

import logging

from arxiv_inspector.indexing import ArxivIndexer

logging.basicConfig(level=logging.DEBUG)
# TEST_ID = '2309.17453'
TEST_ID = '2304.04613'
QDRANT_URL = "http://localhost:6333"
QDRANT_COLLECTION = "arxiv-temp"

PDF_DIR = "/home/sawyer/nas_share/datasets/arxiv/"


def check_file_names_in_dir(directory) -> List[str]:
    """
    Checks to see if every file in the directory follows the arxiv naming convention. Format: 1234.12345.pdf
    :param directory:
    :return:
    """

    bad_files = []

    files = os.listdir(directory)
    for file in files:
        if not re.match(r'\d{4}\.\d{5}\.pdf', file):
            bad_files.append(file)

    return bad_files


if __name__ == "__main__":
    BAD_FILES = check_file_names_in_dir(PDF_DIR)

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
    # indexer.index_arxiv_directory(directory=f"../data/pdfs/")
    indexer.index_arxiv_by_year(directory=PDF_DIR, min_year=2023)

# NEXT: Find out why this isn't adding nodes to the Qdrant database.
