from astrapy import DataAPIClient
from langchain_astradb import AstraDBVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
import pandas as pd
import warnings
# from groq import Groq
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
warnings.filterwarnings("ignore")


def answer_gen(question):
    # ASTRA_DB_APPLICATION_TOKEN = "AstraCS:ZvYLxZLcceZTrcXeEMOxCyDe:dae3b56e90e49af338a11d0ebcf402f7b593e9deaf2d7a6fbcbe429e4de511d7"
    # ASTRA_DB_API_ENDPOINT = "https://67749076-dffb-4c03-905c-15bb314b46c7-us-east-2.apps.astra.datastax.com"  # Replace with your actual endpoint
    # ASTRA_DB_KEYSPACE = "sahai_namespace" # Replace with your actual keyspace
    client = QdrantClient(
    url="https://d120984a-fd16-42a2-bc4e-38a3ecdd3d19.us-west-2-0.aws.cloud.qdrant.io:6333", 
    api_key="tNztKZHHIHLRq0U6LT7pBVyAiR0KYV2oe22hHeAS-FEsyElQznBVxA",
    )
    excel_file_path = 'QAs.xlsx'
    embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    collection_name = "my_collection"
    df = pd.read_excel("QAs.xlsx")

    # vstore = AstraDBVectorStore(
    #     embedding=embeddings,
    #     namespace=ASTRA_DB_KEYSPACE,
    #     collection_name="qna",
    #     token=ASTRA_DB_APPLICATION_TOKEN,
    #     api_endpoint=ASTRA_DB_API_ENDPOINT,
    # )

    query_embedding = embeddings.embed_query(question)
    search_results = client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=1,  # Retrieve the most relevant result
    )
    if search_results:
        best_match = search_results[0]  # Get the best match (most relevant document)
        answer = best_match.payload.get("question")
        row = df[df["Questions"] == answer]
        return row.iloc[0]['Answers']
        # return answer
    else:
        return "No relevant results found."
    # client = Groq(
    #     api_key="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",
    # )

    # chat_completion = client.chat.completions.create(
    #     messages=[
    #         {
    #             "role":"system",
    #             "content":"You have to answer the question only based on the provided data from the chunk."
    #         },
    #         {
    #             "role": "user",
    #             "content": f"Given question \n\n {question} and data \n\n\n {resul}\n\n\n Give the answer only based on the data provided above.",
    #         }
    #     ],
    #     model="llama3-70b-8192",
    #     temperature=0.1
    # )

    # return chat_completion.choices[0].message.content,resul

print(answer_gen("What are the subjects in elective 4"))