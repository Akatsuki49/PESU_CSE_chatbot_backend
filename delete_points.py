from qdrant_client import QdrantClient
from config import *
import os
from qdrant_client.http.models import models

client = QdrantClient(
    url= QDRANT_CLIENT,
    api_key= os.getenv("QDRANT_API_KEY"),
)

def delete_points(ids):
    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector = models.PointIdsList(
            points = ids
        ),
    )
    print("Points deleted successfully")