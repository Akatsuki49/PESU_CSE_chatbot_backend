# from astrapy import DataAPIClient
# from langchain_astradb import AstraDBVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
import pandas as pd
import warnings
# from groq import Groq
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
warnings.filterwarnings("ignore")


def answer_gen(question):
    print(question)
    client = QdrantClient(
    url="https://d120984a-fd16-42a2-bc4e-38a3ecdd3d19.us-west-2-0.aws.cloud.qdrant.io:6333", 
    api_key="tNztKZHHIHLRq0U6LT7pBVyAiR0KYV2oe22hHeAS-FEsyElQznBVxA",
    )
    excel_file_path = 'QAs.xlsx'
    embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    collection_name = "my_collection"
    df = pd.read_excel("QAs.xlsx")

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
        # print(row.iloc[0]['Answers'])
        return row.iloc[0]['Answers']
        # return answer
    else:
        # print("No relevant results found.")
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

if __name__ == "__main__":
    question = "What are the subjects in elective 4"
    print(answer_gen(question))