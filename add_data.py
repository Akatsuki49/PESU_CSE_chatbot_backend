import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer
from config import QDRANT_CLIENT, EMBEDDING_MODEL, COLLECTION_NAME
from store import store_xl


# # Initialize Qdrant client
client = QdrantClient(QDRANT_CLIENT)

# Initialize the embedding model
model = SentenceTransformer(EMBEDDING_MODEL)

# Read Excel file
df = pd.read_excel('QAs.xlsx')

# Fill NaN values with empty strings
df = df.fillna('')

# Ensure the collection exists
if client.collection_exists(collection_name=COLLECTION_NAME):
    # Delete the existing collection
    client.delete_collection(collection_name=COLLECTION_NAME)

store_xl("QAs.xlsx")

# Recreate the collection with the specified vector size and distance metric
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
)

# Prepare points to upload
points = []
for idx, row in df.iterrows():
    question = row['Question']
    answer = row['Answer']
    vector = model.encode(question).tolist()
    payload = {"question": question, "answer": answer}
    point = PointStruct(id=idx, vector=vector, payload=payload)
    points.append(point)

# Upload points to Qdrant
client.upsert(collection_name=COLLECTION_NAME, points=points)

print(f"Uploaded {len(points)} Q&A pairs to the '{COLLECTION_NAME}' collection.")


# from config import QDRANT_CLIENT, EMBEDDING_MODEL, COLLECTION_NAME
# from qdrant_client import QdrantClient

# # Initialize the Qdrant client
# client = QdrantClient(QDRANT_CLIENT)

# # Define the collection name
# collection_name = COLLECTION_NAME

# # Initialize the offset for pagination
# offset = None

# while True:
#     # Retrieve points using the scroll method
#     points, offset = client.scroll(
#         collection_name=collection_name,
#         offset=offset,
#         limit=100,  # Number of points to retrieve per request
#         # with_vectors= True
#     )

#     # Process the retrieved points
#     for point in points:
#         # Access the point ID
#         point_id = point.id

#         # Access the point payload
#         payload = point.payload

#         # Access the point vector (if needed)
#         vector = point.vector

#         # Perform your desired operations with the point data
#         # For example, print the point information
#         print(f"Point ID: {point_id}")
#         print(f"Payload: {payload}")
#         print(f"Vector: {vector}")
#         print('---')

#     # Check if there are more points to retrieve
#     if offset is None:
#         break