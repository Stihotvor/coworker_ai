from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
import chromadb
from llama_index.core.node_parser import (
    SentenceSplitter,
    SemanticSplitterNodeParser,
)
from llama_index.embeddings.openai import OpenAIEmbedding

from src.storage.custom_embedding_clients.lm_studio_client import LMStudioEmbedding

remote_db = chromadb.HttpClient(host="http://localhost:8020")
chroma_collection = remote_db.get_or_create_collection("quickstart")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

embed_model = LMStudioEmbedding(
    base_url="http://localhost:1234/v1",
    model_name="all-MiniLM-L6-v2-ggml-model-f16",
)
splitter = SemanticSplitterNodeParser(
    buffer_size=1, breakpoint_percentile_threshold=95, embed_model=embed_model
)


# load documents
documents = SimpleDirectoryReader("../../data/").load_data()

nodes = splitter.get_nodes_from_documents(documents)
for node in nodes:
    print("### CHUNK ###")
    print(node.get_content())

index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, embed_model=embed_model
)


# define embedding function

# Query Data
# query_engine = index.as_query_engine()
# response = query_engine.query("What are multimodal AI Models?")
# print(response)


#
#
# doc_to_update = chroma_collection.get(limit=1)
# doc_to_update["metadatas"][0] = {
#     **doc_to_update["metadatas"][0],
#     **{"author": "Paul Graham"},
# }
# chroma_collection.update(
#     ids=[doc_to_update["ids"][0]], metadatas=[doc_to_update["metadatas"][0]]
# )
# updated_doc = chroma_collection.get(limit=1)
# print(updated_doc["metadatas"][0])
#
# # delete the last document
# print("count before", chroma_collection.count())
# chroma_collection.delete(ids=[doc_to_update["ids"][0]])
# print("count after", chroma_collection.count())

