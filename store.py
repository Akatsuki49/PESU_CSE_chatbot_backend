from astrapy import DataAPIClient
from langchain_astradb import AstraDBVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
import csv
from langchain_core.documents import Document
import pandas as pd


ASTRA_DB_APPLICATION_TOKEN = "AstraCS:dBtjWDuPxLQlvsovQWBPZJud:4c33db338e67bb3c177c3eb5cea9154bc3d6782ce008090fc94d20b0221f7d54"
ASTRA_DB_API_ENDPOINT = "https://4efc19d7-a22a-4553-bffa-86afd548f4ac-us-east1.apps.astra.datastax.com"  # Replace with your actual endpoint
ASTRA_DB_KEYSPACE = "sahai_namespace"  # Replace with your actual keyspace
excel_file_path = 'QAs.xlsx'
embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)


def read_csv(file_path):
    """Read the content of the CSV file and return question-answer pairs."""
    qa_pairs = []
    df = pd.read_excel(file_path)
    # with open(file_path, 'r', encoding='utf-8') as file:
    for index, row in df.iterrows():
        answer = str(row.iloc[1])  # Assuming the answer is in the second column
        question = str(row.iloc[0]) 
        qa_pairs.append(question + "\n" + answer)
    return qa_pairs

qa = read_csv(excel_file_path)

vstore = AstraDBVectorStore(
    embedding=embeddings,
    namespace=ASTRA_DB_KEYSPACE,
    collection_name="sahaitest",
    token=ASTRA_DB_APPLICATION_TOKEN,
    api_endpoint=ASTRA_DB_API_ENDPOINT,
)

docs = [Document(page_content=chunk) for chunk in qa]
sample_embedding = embeddings.embed_documents([docs[0].page_content])[0]
vstore.add_documents(docs)


