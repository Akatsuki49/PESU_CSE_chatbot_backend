import warnings
import os
import pandas as pd
from langchain_groq import ChatGroq
from config import *
from dotenv import load_dotenv

warnings.filterwarnings("ignore")

# Load environment variables from a .env file if present
load_dotenv()

# Set your Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
groq_client = ChatGroq(
    model=LLM_MODEL,
    temperature=MODEL_TEMPERATURE,
)

def convert_to_markdown(answer):
    messages = [
        ("system", "You are a helpful assistant that converts a given paragraph to a markdown format."),
        ("user", f"Generate a markdown version of the following answer:\n\n'{answer}'\n\n\nDon't output anything like 'here is your response'")
    ]
    return groq_client.invoke(messages).content.strip()

def generate_paraphrases(question, num_paraphrases=30):
    messages = [
        ("system", "You are a helpful assistant that generates paraphrased versions of questions."),
        ("user", f"Generate {num_paraphrases} paraphrased versions of the following question:\n\n'{question}'\n\n\nLet the paraphrases be as unique and variational as possible and generate these paraphrases in a new line each. Don't output anything like 'here is your response'")
    ]
    response = groq_client.invoke(messages)
    paraphrases = response.content.strip().split('\n')
    return [p.strip() for p in paraphrases if p.strip()]

def main():
    # Load the Excel file
    input_file = 'original.xlsx'
    df = pd.read_excel(input_file)

    # Check if 'Answers' column exists
    if 'Answers' not in df.columns:
        raise ValueError("'Answers' column not found in the Excel file.")

    # Convert each answer to Markdown format and store in a new column
    df['Answers_Markdown'] = df['Answers'].apply(convert_to_markdown)

    print("Markdown conversion completed")

    # Generate paraphrases and create a mapping
    qa_mapping = {}
    i = 0
    for index, row in df.iterrows():
        question = row['Questions']
        answer = row['Answers']
        answer_markdown = row['Answers_Markdown']
        if pd.notna(question) and pd.notna(answer):
            paraphrases = generate_paraphrases(question)
            print(f"Generated paraphrase for {i}th question")
            i = i + 1
            for paraphrase in [question] + paraphrases:
                qa_mapping[paraphrase] = (answer, answer_markdown)

    # Convert the mapping to a DataFrame for better visualization
    result_df = pd.DataFrame(
        [(q, ans, ans_md) for q, (ans, ans_md) in qa_mapping.items()],
        columns=['Question', 'Answer', 'Answers_Markdown']
    )
    # Define the output file
    output_file = 'QAs.xlsx'

    # Attempt to read existing data from the output file
    if os.path.exists(output_file):
        existing_df = pd.read_excel(output_file)
        combined_df = pd.concat([existing_df, result_df]).drop_duplicates().reset_index(drop=True)
    else:
        combined_df = result_df

    # Write the combined data to the Excel file
    combined_df.to_excel(output_file, index=False)

    print(f"Markdown conversion and paraphrasing completed. Output saved to '{output_file}'.")

if __name__ == "__main__":
    main()