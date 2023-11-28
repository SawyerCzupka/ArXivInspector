"""
Code to add ArXiv pdf documents to the Qdrant database.
"""

from llama_index.vector_stores import QdrantVectorStore
from llama_index import SimpleDirectoryReader
import os
from typing import List


# function to filter a large directory of arxiv files named YYMM.number.pdf by min and max year. returns
# list of strings
def filter_arxiv_files(directory: str, min_year: int = None, max_year: int = None) -> List[str]:
    """
    Filter a large directory of arxiv files named YYMM.number.pdf by min and max year

    :param directory: directory to filter
    :param min_year: minimum year to filter by (e.g. 2010)
    :param max_year: maximum year to filter by
    :return: list of strings
    """

    # get all files in directory
    files = os.listdir(directory)

    # filter by year
    if min_year is not None:
        files = [file for file in files if int(file[:2]) >= min_year % 100]
    if max_year is not None:
        files = [file for file in files if int(file[:2]) <= max_year % 100]

    # return list of strings
    return files
