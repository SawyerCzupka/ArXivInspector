"""
Indexing module for arxiv_inspector.
"""

from llama_index.vector_stores import QdrantVectorStore
from llama_index.ingestion import IngestionPipeline, IngestionCache
from llama_index.embeddings import HuggingFaceEmbedding

from sentence_transformers import SentenceTransformer
from typing import List


class ArxivIndexer:
    def __init__(
        self,
        vector_store: QdrantVectorStore,
        embedding_model: str = "jinaai/jina-embeddings-v2-base-en",
    ):
        self.vector_store = vector_store
        self.embedding_model = HuggingFaceEmbedding(model_name=embedding_model)

        self.ingestion_pipeline = IngestionPipeline()
        self.ingestion_cache = IngestionCache()

        


    def index_arxiv_pdf(self, pdf_path: str):
        """
        Index an arxiv pdf file

        :param pdf_path: path to pdf file
        :return: None
        """

        pass



    def index_arxiv_directory(self, directory: str):
        """
        Index an entire directory of arxiv pdf files

        :param directory: directory to index
        :return: None
        """
        pass

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
