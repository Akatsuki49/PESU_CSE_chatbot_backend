import dotenv
import os
from config import *
from langchain_community.embeddings import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from rag import validate

dotenv.load_dotenv()
os.environ["QDRANT_API_KEY"] = os.getenv("QDRANT_API_KEY")

embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
collection_name = COLLECTION_NAME

client = QdrantClient(
    url= QDRANT_CLIENT,
    api_key= os.getenv("QDRANT_API_KEY"),
)

def runloop(sheet):
    results = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        question = row[0]  # Assuming the question is in the first column
        answer = row[1]
        if question:
            similar_question = getSimilarQuestions(question)
            finalans = validate(question,similar_question)
            if finalans=="NO":
                results.append({
                    "original_question": question,
                    "original_answer": answer,
                    "similar_question": similar_question
                })

    return results

def getSimilarQuestions(question):
    query_vector = embedding_model.embed_query(question)
    results = client.search(
        collection_name=collection_name, 
        query_vector=query_vector, 
        limit=5,
        with_payload=True)
    
    return results