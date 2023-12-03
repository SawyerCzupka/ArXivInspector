"""
Indexing module for arxiv_inspector.
"""
import os
from typing import List

from llama_index import SimpleDirectoryReader
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.ingestion import IngestionPipeline
from llama_index.node_parser import SimpleFileNodeParser, SimpleNodeParser
from llama_index.vector_stores import QdrantVectorStore

import logging


class ArxivIndexer:
    def __init__(
            self,
            vector_store: QdrantVectorStore,
            embedding_model: str = "jinaai/jina-embeddings-v2-base-en",
    ):
        self.vector_store = vector_store
        # self.embedding_model = HuggingFaceEmbedding(model_name=embedding_model)

        self.ingestion_pipeline = IngestionPipeline(
            transformations=[
                SimpleNodeParser(),
                HuggingFaceEmbedding(model_name=embedding_model, embed_batch_size=2)
            ],
            vector_store=self.vector_store
        )

    def index_arxiv_pdf(self, pdf_path: str):
        """
        Index an arxiv pdf file

        :param pdf_path: path to pdf file
        :return: None
        """
        reader = SimpleDirectoryReader(input_files=[pdf_path])
        docs = reader.load_data(show_progress=True)

        self.ingestion_pipeline.run(documents=docs, show_progress=True)

    def index_arxiv_directory(self, directory: str):
        """
        Index an entire directory of arxiv pdf files

        :param directory: directory to index
        :return: None
        """

        reader = SimpleDirectoryReader(directory)
        docs = reader.load_data(show_progress=True)

        self.ingestion_pipeline.run(documents=docs, show_progress=True)

    def index_arxiv_file_list(self, file_list: List[str], directory: str):
        """
        Index a list of arxiv pdf files

        :param file_list: list of files to index
        :param directory: directory of files
        :return: None
        """
        pass


if __name__ == "__main__":
    pass
