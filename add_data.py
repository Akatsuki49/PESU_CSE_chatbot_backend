import pandas as pd
import time
import os
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer
from config import QDRANT_CLIENT_1, EMBEDDING_MODEL, COLLECTION_NAME, FILE_PATH

# Initialize Qdrant client
client = QdrantClient(
    url=QDRANT_CLIENT_1,
    api_key=os.getenv("QDRANT_API_KEY"),
)

# Initialize the embedding model
model = SentenceTransformer(EMBEDDING_MODEL)

# Read Excel file
df = pd.read_excel(FILE_PATH)

# Fill NaN values with empty strings
df = df.fillna('')

# Ensure the collection exists; if it does, delete it
if client.collection_exists(collection_name=COLLECTION_NAME):
    client.delete_collection(collection_name=COLLECTION_NAME)

# Recreate the collection with the specified vector size and distance metric
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
)

# Define batch size
batch_size = 1000

# Function to process and upload a batch of data
def process_batch(batch_df, start_idx):
    points = []
    for idx, row in batch_df.iterrows():
        question = row['Question']
        answer = row['Answer']
        answer_markdown = row['Answers_Markdown']
        vector = model.encode(question).tolist()
        payload = {"question": question, "answer": answer, "markdown": answer_markdown}
        point = PointStruct(id=start_idx + idx, vector=vector, payload=payload)
        points.append(point)
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Uploaded {len(points)} Q&A pairs starting from ID {start_idx} to the '{COLLECTION_NAME}' collection.")

# Process data in batches
for start_idx in range(0, len(df), batch_size):
    end_idx = min(start_idx + batch_size, len(df))
    batch_df = df.iloc[start_idx:end_idx]
    process_batch(batch_df, start_idx)
    
    # Clear cache if using lru_cache
    if hasattr(model.encode, 'cache_clear'):
        model.encode.cache_clear()
        print("Cache cleared.")


print("All data has been processed and uploaded.")