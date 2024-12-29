from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
import warnings
from qdrant_client import QdrantClient
from langchain_groq import ChatGroq
import dotenv
import os
warnings.filterwarnings("ignore")

dotenv.load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["QDRANT_API_KEY"] = os.getenv("QDRANT_API_KEY")

qdrant_client_url = "https://d120984a-fd16-42a2-bc4e-38a3ecdd3d19.us-west-2-0.aws.cloud.qdrant.io:6333"

quadrant_client = QdrantClient(
    url= qdrant_client_url, 
    api_key= os.getenv("QDRANT_API_KEY"),
    )

excel_file_path = 'QAs.xlsx'
embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
collection_name = "pesu_cse_qa_collection"

groq_client = ChatGroq(
        model="llama3-70b-8192",
        temperature=0.1,
    )

def retrieve_ans(question):
    query_embedding = embeddings.embed_query(question)
    search_results = quadrant_client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=1,  # Retrieve the most relevant result
        with_payload=True,
        score_threshold=0.8
    )
    # print(search_results)
    if search_results:
        best_match = search_results[0]  # Get the best match (most relevant document)
        ques = best_match.payload.get("question")
        relevant_ans = best_match.payload.get("answer")
        return relevant_ans
    else:
        return "No relevant results found."
    
def call_llm(question, relevant_ans):
    if relevant_ans == "No relevant results found.":
        return "No relevant results found."
    messages=[
        ("system", "You are a user friendly responder bot answering on behalf of the PES University RR Campus Bengaluru, BTech CSE department."),
        ("user", f"Given question \n\n {question} and answer to this question: \n\n\n {relevant_ans}\n\n\n Structure the answer better and give a more user friendly response"),
    ]
    return groq_client.invoke(messages).content

if __name__ == "__main__":
    question = "What are the subjects in elective 4"
    relevant_ans = retrieve_ans(question)
    print(call_llm(question, relevant_ans))
    