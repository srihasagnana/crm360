
from functools import lru_cache
from pathlib import Path

import chromadb
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=1)
def get_rag_components():
    project_root = Path(__file__).resolve().parents[2]
    knowledge_path = project_root / "rag_experiments" / "retention_knowledge.txt"

    documents = TextLoader(str(knowledge_path)).load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    chunks = splitter.split_text(documents[0].page_content)

    if not chunks:
        raise ValueError("Retention knowledge base is empty.")

    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(
        path=str(project_root / "crm360_chroma_db")
    )

    collection = client.get_or_create_collection(
        name="crm360_retention_v2"
    )

    if collection.count() == 0:
        embeddings = embedding_model.encode(chunks)

        collection.add(
            ids=[f"retention_{i}" for i in range(len(chunks))],
            embeddings=embeddings.tolist(),
            documents=chunks
        )

    return embedding_model, collection


def retrieve_retention_guidance(query, n_results=3):
    embedding_model, collection = get_rag_components()

    query_embedding = embedding_model.encode(query)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=min(n_results, collection.count())
    )

    return results["documents"][0]
