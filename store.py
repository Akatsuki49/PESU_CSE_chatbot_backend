from astrapy import DataAPIClient
from langchain_astradb import AstraDBVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
import csv
from langchain_core.documents import Document
import pandas as pd
import pickle


ASTRA_DB_APPLICATION_TOKEN = "AstraCS:ZvYLxZLcceZTrcXeEMOxCyDe:dae3b56e90e49af338a11d0ebcf402f7b593e9deaf2d7a6fbcbe429e4de511d7"
ASTRA_DB_API_ENDPOINT = "https://67749076-dffb-4c03-905c-15bb314b46c7-us-east-2.apps.astra.datastax.com"  # Replace with your actual endpoint
ASTRA_DB_KEYSPACE = "sahai_namespace"  # Replace with your actual keyspace
excel_file_path = 'QAs.xlsx'
embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

vstore = AstraDBVectorStore(
    embedding=embeddings,
    namespace=ASTRA_DB_KEYSPACE,
    collection_name="qna",
    token=ASTRA_DB_APPLICATION_TOKEN,
    api_endpoint=ASTRA_DB_API_ENDPOINT,
)

QA_DICT_PATH = "qa_dict.pkl"

def read_csv(file_path):
    """Read the content of the CSV file and return question-answer pairs."""
    questions = []
    answers = []
    df = pd.read_excel(file_path)
    # with open(file_path, 'r', encoding='utf-8') as file:
    for index, row in df.iterrows():
        answer = str(row.iloc[1])  # Assuming the answer is in the second column
        question = str(row.iloc[0]) 
        questions.append(question)
        answers.append(answer)
    return questions, answers

def segregate(questions, answers):
    qa = dict()
    docs = []
    for question, answer in zip(questions, answers):
        qa[question] = answer
        docs.append(Document(page_content=question))
    return qa, docs

if __name__ == "__main__":
    questions, answers = read_csv(excel_file_path)
    qa, docs = segregate(questions, answers)
    vstore.add_documents(docs)

    with open(QA_DICT_PATH, 'wb') as f:
        pickle.dump(qa, f)

# docs = [Document(page_content=chunk) for chunk in qa]
# sample_embedding = embeddings.embed_documents([docs[0].page_content])[0]
# vstore.add_documents(docs)


