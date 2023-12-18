"""
Indexing module for arxiv_inspector.
"""
import os
from typing import List

from llama_index import SimpleDirectoryReader
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.ingestion import IngestionPipeline
from llama_index.node_parser import SimpleNodeParser
from llama_index.vector_stores import QdrantVectorStore

import logging
from tqdm import tqdm


class ArxivIndexer:
    def __init__(
            self,
            vector_store: QdrantVectorStore,
            embedding_model: str = "jinaai/jina-embeddings-v2-base-en",
    ):
        self.vector_store = vector_store
        self.ingestion_pipeline = IngestionPipeline(
            transformations=[
                SimpleNodeParser(chunk_size=512),
                HuggingFaceEmbedding(model_name=embedding_model, embed_batch_size=3, trust_remote_code=True)
            ],
            vector_store=self.vector_store
        )

    def index_arxiv_pdf(self, pdf_path: str):
        """
        Index an arxiv pdf file

        :param pdf_path: path to pdf file
        :return: None
        """
        logging.info(f"Indexing file: {pdf_path}")
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
        logging.info(f"Indexing {len(file_list)} files from list")

        for file in tqdm(file_list):
            file_path = os.path.join(directory, file)
            self.index_arxiv_pdf(file_path)

    def index_arxiv_by_year(self, directory: str, min_year: int = 2020, max_year: int = None):
        """
        Index all arxiv pdf files by year using the arxiv identifier. Format: YYMM.NNNNN
        TODO - use DB for date instead of filename

        :param directory: directory to index
        :param min_year: minimum year to index. YYYY format
        :param max_year: maximum year to index. YYYY format
        :return: None
        """
        logging.info(f"Indexing arxiv files from {min_year} to {max_year}")

        file_names_in_dir = [path for path in os.listdir(directory)]
        files_to_index = []

        for file_name in file_names_in_dir:
            # logging.info(f"Checking file: {file_name}")
            file_year = int(file_name.split('.')[0][:2]) + 2000
            if file_year >= min_year:
                if max_year is not None:
                    if file_year <= max_year:
                        files_to_index.append(file_name)
                else:
                    files_to_index.append(file_name)

        self.index_arxiv_file_list(file_list=files_to_index, directory=directory)


if __name__ == "__main__":
    pass
