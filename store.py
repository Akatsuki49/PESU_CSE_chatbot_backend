from langchain_community.embeddings import HuggingFaceEmbeddings
import warnings
from langchain_core.documents import Document
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import os
import uuid
import dotenv
from config import *
warnings.filterwarnings("ignore")

dotenv.load_dotenv()
os.environ["QDRANT_API_KEY"] = os.getenv("QDRANT_API_KEY")

embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
collection_name = COLLECTION_NAME

client = QdrantClient(
    url= QDRANT_CLIENT,
    api_key= os.getenv("QDRANT_API_KEY"),
)

def generate_custom_uuid():
    return str(uuid.uuid4())

def store_xl(excel_file_path):

    # if client.collection_exists(collection_name):
    #     client.delete_collection(collection_name)

    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

    def read_csv(file_path):
        """Read the content of the CSV file and return question-answer pairs."""
        questions = []
        answers = []
        df = pd.read_excel(file_path)
        for index, row in df.iterrows():
            answer = str(row.iloc[1])
            question = str(row.iloc[0]) 
            questions.append(question)
            answers.append(answer)

        #delete file at excel_file_path
        if os.path.exists(excel_file_path):
            os.remove(excel_file_path)
        
        return questions, answers

    def segregate(questions, answers):
        qa = dict()
        docs = []
        for question, answer in zip(questions, answers):
            qa[question] = answer
            docs.append(Document(page_content=question))
        return qa, docs

    questions, answers = read_csv(excel_file_path)
    qa, docs = segregate(questions, answers)
    doc_embeddings = embedding_model.embed_documents([doc.page_content for doc in docs])

    points = [
        PointStruct(
            id=generate_custom_uuid(),
            vector=embedding,
            payload={"question": questions[idx], "answer": answers[idx]},
        )
        for idx, embedding in enumerate(doc_embeddings)
    ]

    client.upsert(
        collection_name=collection_name,
        points=points
    )
    
    print("Successfully ingested documents into Qdrant VDB and stored QA in PKL File")

def store_single_qa(question, answer):
    question_doc = Document(page_content=question)
    doc_embedding = embedding_model.embed_documents([question_doc.page_content])

    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

    client.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(
                id=generate_custom_uuid(),
                vector=doc_embedding[0],
                payload={"question": question, "answer": answer},
            )
        ]
    )

# if __name__ == "__main__":
#     file_to_store = r"C:\Users\sowme\StudioProjects\PESU_CSE_chatbot_backend\QAs.xlsx"
#     store_xl(file_to_store)


