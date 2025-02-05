import dotenv
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from qdrant_client import QdrantClient

dotenv.load_dotenv()
os.environ["QDRANT_API_KEY"] = os.getenv("QDRANT_API_KEY")

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
collection_name = "pesu_cse_qa_collection"

qdrant_client_url = "https://d120984a-fd16-42a2-bc4e-38a3ecdd3d19.us-west-2-0.aws.cloud.qdrant.io:6333"

client = QdrantClient(
    url= qdrant_client_url,
    api_key= os.getenv("QDRANT_API_KEY"),
)

def getSimilarQuestions(question):
    query_vector = embedding_model.embed_query(question)
    results = client.search(collection_name=collection_name, query_vector=query_vector, limit=5)
    return results