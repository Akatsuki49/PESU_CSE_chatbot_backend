from astrapy import DataAPIClient
from langchain_astradb import AstraDBVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
import csv
from langchain_core.documents import Document
import pandas as pd
from groq import Groq

def answer_gen(question):
    ASTRA_DB_APPLICATION_TOKEN = "AstraCS:ZvYLxZLcceZTrcXeEMOxCyDe:dae3b56e90e49af338a11d0ebcf402f7b593e9deaf2d7a6fbcbe429e4de511d7"
    ASTRA_DB_API_ENDPOINT = "https://67749076-dffb-4c03-905c-15bb314b46c7-us-east-2.apps.astra.datastax.com"  # Replace with your actual endpoint
    ASTRA_DB_KEYSPACE = "sahai_namespace" # Replace with your actual keyspace
    # excel_file_path = 'QAs.xlsx'
    embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)


    vstore = AstraDBVectorStore(
        embedding=embeddings,
        namespace=ASTRA_DB_KEYSPACE,
        collection_name="qna",
        token=ASTRA_DB_APPLICATION_TOKEN,
        api_endpoint=ASTRA_DB_API_ENDPOINT,
    )

    resul = []
    results = vstore.similarity_search(str(question), k=1)
    for res in results:
        resul.append(res.page_content)
    
    client = Groq(
        api_key="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",
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role":"system",
                "content":"You have to answer the question only based on the provided data from the chunk."
            },
            {
                "role": "user",
                "content": f"Given question \n\n {question} and data \n\n\n {resul}\n\n\n Give the answer only based on the data provided above.",
            }
        ],
        model="llama3-70b-8192",
        temperature=0.1
    )

    return chat_completion.choices[0].message.content,resul

print(answer_gen("What are the subjects in elective 4"))