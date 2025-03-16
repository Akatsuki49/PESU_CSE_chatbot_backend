from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
import warnings
from qdrant_client import QdrantClient
from langchain_groq import ChatGroq
import dotenv
import os
from config import *
warnings.filterwarnings("ignore")

dotenv.load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["QDRANT_API_KEY"] = os.getenv("QDRANT_API_KEY")

quadrant_client = QdrantClient(
    url= QDRANT_CLIENT, 
    api_key= os.getenv("QDRANT_API_KEY"),
    )

excel_file_path = FILE_PATH 
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
collection_name = COLLECTION_NAME

groq_client = ChatGroq(
        model=LLM_MODEL,
        temperature=MODEL_TEMPERATURE,
    )

def retrieve_ans(question):
    prof = profanity(question)
    # print(prof)
    if prof==0:
        query_embedding = embeddings.embed_query(question)
        search_results = quadrant_client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=10,  # Retrieve the most relevant result
            with_payload=True,
            # score_threshold = 0.5
        )
        # print(search_results)
        best_match = finalize(search_results, question)  # Get the best match (most relevant document)
        # print(best_match)
        # best_match = 0
        if best_match!=100:
            ques = search_results[best_match].payload["question"]
            relevant_ans = search_results[best_match].payload["answer"]
            return relevant_ans, call_llm(ques, relevant_ans)
        else:
            return "No relevant results found.", "No relevant results found."
    else:
        return "Please avoid using inappropriate language!", "Please avoid using inappropriate language!"
    
def profanity(question):
    messages=[
        ("system", "You are a strict profanity checker agent."),
        ("user", f"Given question \n\n {question}\n, check if this question is vulgar or inappropriate. If yes, output 1 else 0. Only output the number nothing else."),
    ]
    return int(groq_client.invoke(messages).content.strip())

def call_llm(question, relevant_ans):
    if relevant_ans == "No relevant results found.":
        return "No relevant results found."
    messages=[
        ("system", "You are a user friendly responder bot answering on behalf of the PES University RR Campus Bengaluru, BTech CSE department."),
        ("user", f"Given question \n\n {question} and answer to this question: \n\n\n {relevant_ans}\n\n\n Structure the answer better and give a more user friendly response, dont add anything like 'here is your response' , give straightforward response."),
    ]
    return groq_client.invoke(messages).content

def finalize(search_results, question):
    if not search_results:
        raise ValueError("search_results list is empty.")

    # Extract questions from search results safely
    extracted_questions = []
    for i, result in enumerate(search_results[:10]):  # Limit to top 3 results
        payload = result.payload if hasattr(result, 'payload') else {}
        q = payload.get("question", f"Question {i+1} not available.")
        extracted_questions.append(f"{i} - {q}")

    # Construct the prompt
    prompt = f'''
    Given the original question : "{question}" \n\n
    and the top 10 similar questions:
    {'\n'.join(extracted_questions)}\n\n
    Is any of similar question's intent same as original question? If yes, output the number corresponding to the question (take into account 0 based indexing of numbers corresponding to the question). If nothing as such is found, output 100. Only output the number, nothing else.
    '''
    # print(prompt)
    messages = [
        {"role": "system", "content": "You are a strict question similarity checker that gives the index of the question which is similar to the original question"},
        {"role": "user", "content": prompt},
    ]

    return int(groq_client.invoke(messages).content.strip())

def validate(question, similar_question):
    messages=[
        ("system", "You are a user friendly responder bot answering on behalf of the PES University RR Campus Bengaluru, BTech CSE department."),
        ("user", f"Given the main question \n\n {question} and top 5 similar questions: \n\n\n {similar_question}\n\n\n Looking at these similar questions and the main question, is any of the similar question's intent same as the main question? Output only YES or NO"),
    ]
    return groq_client.invoke(messages).content

if __name__ == "__main__":
    question = "subjects in 10th elective"
    relevant_ans = retrieve_ans(question)
    print(relevant_ans)
    # print(call_llm(question, relevant_ans))
    