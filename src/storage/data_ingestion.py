import os
from typing import Type, List, Literal

from llama_index.core import Settings, Document, SimpleDirectoryReader
from llama_index.core.ingestion import IngestionCache, IngestionPipeline
from llama_index.storage.kvstore.redis import RedisKVStore
from llama_index.vector_stores.chroma import ChromaVectorStore

DOCUMENT_PATHS = {
    "tickets": "../../data/tickets",
    "documentation": "../../data/documentation"
}


class DataIngestionManager:
    """
    Interface for data ingestion process. Manages the data transformation and ingestion into the vector store.

    Usage:
        ingest_manager = DataIngestionManager()
        ingest_manager.run_ingestion_pipeline()
    """

    def __init__(self,
                 vector_store: "ChromaVectorStore",
                 settings: "Settings" = Settings,
                 ingestion_pipeline: Type["IngestionPipeline"] = IngestionPipeline,
                 ingest_cache: Type["IngestionCache"] = IngestionCache,
                 cache_client: Type["RedisKVStore"] = RedisKVStore,
                 cache_collection: str = "redis_cache_collection",
                 ):
        self._vector_store = vector_store
        self._ingestion_pipeline = ingestion_pipeline
        self._settings = settings
        self._ingest_cache = self._setup_cache(ingest_cache, cache_client, cache_collection)

    def run_ingestion_pipeline(self, document_type: Literal["tickets", "documentation"]):
        documents = self._load_documents(dir_path=DOCUMENT_PATHS[document_type])
        self._run_ingestion_pipeline(documents)

    def _run_ingestion_pipeline(self, documents: List[Document]):
        pipeline = self._ingestion_pipeline(
            vector_store=self._vector_store,
            cache=self._ingest_cache,
        )
        pipeline.run(documents=documents, show_progress=True)

    def _setup_cache(self, ingest_cache: Type["IngestionCache"], cache_client: Type["RedisKVStore"],
                     cache_collection: str) -> "IngestionCache":
        kwargs = {
            "cache": cache_client.from_host_and_port(
                host=os.getenv("REDIS_HOST"),
                port=int(os.getenv("REDIS_PORT"))
            ),
            "collection": cache_collection
        }
        return ingest_cache(**kwargs)

    def _load_documents(self, dir_path: str) -> List[Document]:
        return SimpleDirectoryReader(dir_path).load_data()
