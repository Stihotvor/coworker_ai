import logging
import os
from typing import Type, List, Literal

from llama_index.core import Settings, Document, SimpleDirectoryReader
from llama_index.core.ingestion import IngestionCache, IngestionPipeline
from llama_index.storage.kvstore.redis import RedisKVStore
from llama_index.vector_stores.chroma import ChromaVectorStore

log = logging.getLogger("storageLogger.data_ingestion")

DOCUMENT_PATHS = {
    "tickets": "data/tickets",
    "documentation": "data/documentation"
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
                 ingestion_pipeline_cls: Type["IngestionPipeline"] = IngestionPipeline,
                 ingest_cache_cls: Type["IngestionCache"] = IngestionCache,
                 cache_client_cls: Type["RedisKVStore"] = RedisKVStore,
                 cache_collection: str = "redis_cache_collection",
                 ):
        log.info("DataIngestionManager initialization")
        self._vector_store = vector_store
        self._ingestion_pipeline_cls = ingestion_pipeline_cls
        self._settings = settings
        self._ingest_cache = self._setup_cache(ingest_cache_cls, cache_client_cls, cache_collection)
        log.info("DataIngestionManager initialized")

    def run_ingestion_pipeline(self, document_type: Literal["tickets", "documentation"]):
        log.info(f"Running ingestion pipeline for {document_type}")
        documents = self._load_documents(dir_path=DOCUMENT_PATHS[document_type])
        self._run_ingestion_pipeline(documents, document_type=document_type)
        log.info(f"Ingestion pipeline completed for {document_type}")

    def _run_ingestion_pipeline(self, documents: List[Document], document_type: str) -> None:
        log.debug(f"Running ingestion pipeline for {document_type}")
        pipeline = self._ingestion_pipeline_cls(
            vector_store=self._vector_store,
            cache=self._ingest_cache,
        )
        # Print collection to logs
        log.debug(f"Collection: {pipeline.vector_store.collection_name}")

        pipeline.run(documents=documents, show_progress=True, document_type=document_type)
        log.debug(f"Ingestion pipeline completed for {document_type}")

    def _setup_cache(self, ingest_cache: Type["IngestionCache"], cache_client: Type["RedisKVStore"],
                     cache_collection: str) -> "IngestionCache":
        log.debug("Setting up the cache for ingestion pipeline")
        kwargs = {
            "cache": cache_client.from_host_and_port(
                host=os.getenv("REDIS_HOST"),
                port=int(os.getenv("REDIS_PORT"))
            ),
            "collection": cache_collection
        }
        return ingest_cache(**kwargs)

    def _load_documents(self, dir_path: str) -> List[Document]:
        log.debug(f"Loading documents from {dir_path}")
        return SimpleDirectoryReader(dir_path).load_data()
