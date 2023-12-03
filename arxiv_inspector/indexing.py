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

    def index_arxiv_by_year(self, directory: str, min_year: int = 2020, max_year: int = None):
        """
        Index all arxiv pdf files by year using the arxiv identifier. Format: YYMM.NNNNN

        :param directory: directory to index
        :param min_year: minimum year to index. YYYY format
        :param max_year: maximum year to index. YYYY format
        :return: None
        """

        file_names_in_dir = os.listdir(directory)
        files_to_index = []

        for file_name in file_names_in_dir:
            file_year = int(file_name.split('.')[0][:2]) * 100
            if file_year >= min_year:
                if max_year is not None:
                    if file_year <= max_year:
                        files_to_index.append(file_name)
                else:
                    files_to_index.append(file_name)

        self.index_arxiv_file_list(file_list=files_to_index, directory=directory)


if __name__ == "__main__":
    pass
