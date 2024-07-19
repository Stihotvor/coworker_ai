import os
from typing import Type, Literal

import chromadb
from chromadb import ClientAPI
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.chat_engine.types import ChatMode, BaseChatEngine
from llama_index.vector_stores.chroma import ChromaVectorStore

from src.storage.data_ingestion import DataIngestionManager


class VectorStoreIndexManager:
    def __init__(self,
                 document_type: Literal["tickets", "documentation"],
                 vector_db: "chromadb" = chromadb,
                 vector_store_cls: Type["ChromaVectorStore"] = ChromaVectorStore,
                 vector_store_index_cls: Type["VectorStoreIndex"] = VectorStoreIndex,
                 storage_context_cls: Type["StorageContext"] = StorageContext,
                 data_ingest_manager_cls: Type["DataIngestionManager"] = DataIngestionManager
                 ):
        self._db_client = self._get_vector_db_client(vector_db)
        self._document_type = document_type
        self._collection_name = self._get_collection_name()
        collection = self._get_or_create_collection()
        self._vector_store = vector_store_cls(chroma_collection=collection)
        self._storage_context = storage_context_cls.from_defaults(vector_store=self._vector_store)
        self._data_ingest_manager = data_ingest_manager_cls(vector_store=self._vector_store,
                                                            cache_collection=self._collection_name)
        self._index = self._get_index(vector_store_index_cls)

    def get_index(self) -> "VectorStoreIndex":
        return self._index

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
        # TODO: Add all the necessary parameters to the method

        # TODO: Add context template
        context_template = None

        return self._index.as_chat_engine(
            system_prompt="Always answer in rhymes.",
            context_template=context_template,
            chat_mode=ChatMode.CONTEXT,
            streaming=True,
            filters=None,
            similarity_top_k=3,
            vector_store_kwargs={
                "where": None,
            }
        )

    def reindex_documents(self):
        self._remove_documents()
        self._get_or_create_collection()
        self._load_documents()

    def _remove_documents(self):
        self._db_client.delete_collection(self._collection_name)

    def _load_documents(self):
        self._data_ingest_manager.run_ingestion_pipeline(document_type=self._document_type)

    def _get_vector_db_client(self, vector_db: "chromadb" = chromadb) -> "ClientAPI":
        chroma_host = os.getenv("CHROMA_HOST")
        chroma_port = os.getenv("CHROMA_PORT")
        vector_db_host = ":".join([chroma_host, chroma_port])
        return vector_db.HttpClient(host=vector_db_host)

    def _get_or_create_collection(self):
        return self._db_client.get_or_create_collection(self._collection_name)

    def _get_index(self, vector_store_index_cls: Type["VectorStoreIndex"]):
        return vector_store_index_cls.from_vector_store(
            vector_store=self._vector_store,
            storage_context=self._storage_context
        )

    def _get_collection_name(self) -> str:
        return f"{self._document_type}_collection"
