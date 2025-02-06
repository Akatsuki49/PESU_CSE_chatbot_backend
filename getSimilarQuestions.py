import dotenv
import os
from config import *
from langchain_community.embeddings import HuggingFaceEmbeddings
from qdrant_client import QdrantClient

dotenv.load_dotenv()
os.environ["QDRANT_API_KEY"] = os.getenv("QDRANT_API_KEY")

embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
collection_name = COLLECTION_NAME

client = QdrantClient(
    url= QDRANT_CLIENT,
    api_key= os.getenv("QDRANT_API_KEY"),
)

def getSimilarQuestions(question):
    query_vector = embedding_model.embed_query(question)
    results = client.search(
        collection_name=collection_name, 
        query_vector=query_vector, 
        limit=5,
        with_payload=True)
    
    print(results)
    
    return results