import random
import string
from typing import cast

import chromadb
import redis
from chromadb import EmbeddingFunction, Documents, Embeddings
from fastapi import FastAPI, HTTPException

app = FastAPI()


class LMStudioEmbeddingServer(EmbeddingFunction[Documents]):
    def __init__(self, url: str):
        try:
            import requests
        except ImportError:
            raise ValueError(
                "The requests python package is not installed. Please install it with `pip install requests`"
            )
        self._api_url = f"{url}"
        self._session = requests.Session()

    def __call__(self, input: Documents) -> Embeddings:
        # Call HuggingFace Embedding Server API for each document
        result = cast(
            Embeddings, self._session.post(self._api_url, json={"input": input}).json()['data']
        )
        result = [item['embedding'] for item in result]
        for item in result:
            print(f"Received embedding with dimension: {len(item)}")

        print(f"Embeddings: {result}")
        return result


# Global variables for ChromaDB client and collection
chroma_client = None
chroma_collection = None


@app.on_event("startup")
async def startup_event():
    global chroma_client, chroma_collection
    huggingface_ef = LMStudioEmbeddingServer(url="http://host.docker.internal:1234/v1/embeddings")

    try:
        chroma_client = chromadb.HttpClient(host="chromadb", port=8000)
        try:
            chroma_client.get_collection("test-collection", embedding_function=huggingface_ef)
            chroma_client.delete_collection("test-collection")
        except Exception as e:
            print(f"Collection not found: {e}")
        chroma_collection = chroma_client.create_collection("test-collection", embedding_function=huggingface_ef)
    except Exception as e:
        print(f"Unable to connect to ChromaDB or create/get collection: {e}")


# Create healthcheck endpoint
@app.get("/healthcheck/")
def healthcheck():
    return {"status": "ok"}


@app.get("/test_redis")
def test_redis():
    try:
        r = redis.Redis(host='redis', port=6379, db=0)
        r.ping()
        return {"message": "Connected to Redis successfully!"}
    except redis.exceptions.ConnectionError:
        raise HTTPException(status_code=500, detail="Unable to connect to Redis")


@app.get("/test_chromadb")
def test_chromadb():
    try:
        # Generate random data
        doc_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        doc_text = "This is a test document " + doc_id
        chroma_collection.add(
            documents=[doc_text],
            metadatas=[{"source": "test"}],
            ids=[doc_id],
        )
        results = chroma_collection.query(
            query_texts=[doc_id],
            n_results=1
        )
        return {"message": "Added and retrieved a document from ChromaDB successfully!", "results": results}
    except Exception as e:
        print(f"Unable to add/retrieve document from ChromaDB: {e}")
        raise HTTPException(status_code=500, detail="Unable to add/retrieve document from ChromaDB")
