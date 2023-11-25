# ArxivInspector

Welcome to ArxivInspector, a specialized project designed to create a daily digest of research papers from ArXiv, employing a Retrieval Augmented Generation (RAG) approach. This project is particularly focused on minimizing false negatives, ensuring a comprehensive collection of relevant research papers, and providing insights into both current trends and future directions in key research areas.
Project Overview

ArxivInspector utilizes a RAG system to enhance the process of generating summaries from ArXiv research papers. This system is updated daily to include the latest publications, and it employs advanced text embeddings stored in a Qdrant database for efficient retrieval and information synthesis.

## Key Features

- Daily Research Digest: Automated system for daily updates with the latest ArXiv papers.
- Minimized False Negatives: High priority on comprehensive coverage, even at the expense of some less relevant inclusions.
- Retrieval Augmented Generation: Utilizes a RAG framework for effective information synthesis and summarization.
- Qdrant Database: Advanced storage and retrieval of text embeddings for efficient processing.

## Realistic Objective and Scope

- Objective: Develop a RAG system for daily updates of ArXiv research papers.
- Scope: The system will focus on ArXiv papers within specific tags: "cs.CV" (Computer Vision), "cs.AI" (Artificial Intelligence), "cs.LG" (Machine Learning), "cs.CL" (Computational Linguistics), "cs.NE" (Neural and Evolutionary Computing), and "stat.ML" (Machine Learning Statistics), starting from 2015.

## Tools and Technologies

- LlamaIndex: An indexing tool for managing research papers.
- Mistral 7B: A model for advanced content processing and understanding.
- Jina AI Embeddings: For creating rich and contextual embeddings.
- Qdrant Database: For storing and retrieving text embeddings efficiently.
