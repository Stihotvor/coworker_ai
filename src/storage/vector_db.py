import logging
import os
from typing import Type

import chromadb
from chromadb import ClientAPI
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.chat_engine.types import ChatMode, BaseChatEngine
from llama_index.vector_stores.chroma import ChromaVectorStore

from src.storage.data_ingestion import DataIngestionManager

log = logging.getLogger("storageLogger.vector_db")


class VectorStoreIndexManager:
    def __init__(self,
                 vector_db: "chromadb" = chromadb,
                 vector_store_cls: Type["ChromaVectorStore"] = ChromaVectorStore,
                 vector_store_index_cls: Type["VectorStoreIndex"] = VectorStoreIndex,
                 storage_context_cls: Type["StorageContext"] = StorageContext,
                 data_ingest_manager_cls: Type["DataIngestionManager"] = DataIngestionManager
                 ):
        log.info("Initializing VectorStoreIndexManager")
        self._collection_name = "docs_and_tickets_collection"
        self._db_client = self._get_db_client(vector_db)
        self._data_ingest_manager_cls = data_ingest_manager_cls
        self._vector_store_index_cls = vector_store_index_cls
        self._vector_store_cls = vector_store_cls
        self._storage_context_cls = storage_context_cls
        log.info("VectorStoreIndexManager initialized successfully")

    def get_index(self) -> "VectorStoreIndex":
        log.info("Getting the index")
        return self._get_index()

    def get_chat_engine(self) -> "BaseChatEngine":
        """
        Usage:
            response: StreamingAgentChatResponse = chat_engine.stream_chat(
                message="Where is the reference file is located?",
                chat_history=[
                    ChatMessage(role="user", content="Tell me about the AI models that are multimodal."),
                    ChatMessage(role="assistant", content="Let me check that for you."),
                ]
            )
            # print(response)
            for text in response.response_gen:
                print(text, end="", flush=True)
        """
        log.info("Getting the chat engine")
        # TODO: Add all the necessary parameters to the method

        # TODO: Add context template
        context_template = None

        index = self.get_index()
        return index.as_chat_engine(
            system_prompt="Always answer in rhymes.",
            context_template=context_template,
            chat_mode=ChatMode.CONTEXT,
            streaming=True,
            filters=None,
            similarity_top_k=8,
            vector_store_kwargs={
                "where": None,
            }
        )

    def reindex_documents(self):
        log.info("Re-indexing documents")
        self._remove_documents()
        self._get_or_create_collection()
        self._load_documents()
        log.info("Documents re-indexed successfully")

    def _remove_documents(self):
        log.debug("Removing documents")
        try:
            self._db_client.delete_collection(self._collection_name)
            log.debug("Documents removed successfully")
        except Exception as error:
            if error.args[0] != f"Collection {self._collection_name} does not exist.":
                raise

            log.debug(f"Collection {self._collection_name} not found")

    def _load_documents(self):
        log.debug("Loading documents")
        data_ingest_manager = self._data_ingest_manager_cls(vector_store=self._get_vector_store(),
                                                            cache_collection=self._collection_name)

        for document_type in ["tickets", "documentation"]:
            log.debug(f"Loading {document_type} documents")
            data_ingest_manager.run_ingestion_pipeline(document_type=document_type)

        log.debug("Documents loaded successfully")

    def _get_db_client(self, vector_db: "chromadb" = chromadb) -> "ClientAPI":
        log.debug("Getting the vector db client")
        chroma_host = os.getenv("CHROMADB_HOST")
        chroma_port = os.getenv("CHROMADB_PORT")
        return vector_db.HttpClient(host=chroma_host, port=chroma_port)

    def _get_or_create_collection(self):
        log.debug(f"Getting or creating the collection: {self._collection_name}")
        return self._db_client.get_or_create_collection(self._collection_name)

    def _get_vector_store(self):
        log.debug("Getting the vector store")
        collection = self._get_or_create_collection()
        return self._vector_store_cls.from_collection(collection=collection)

    def _get_storage_context(self):
        log.debug("Getting the storage context")
        return self._storage_context_cls.from_defaults(vector_store=self._get_vector_store())

    def _get_index(self):
        log.debug("Getting the index")
        return self._vector_store_index_cls.from_vector_store(
            vector_store=self._get_vector_store(),
            storage_context=self._get_storage_context()
        )
