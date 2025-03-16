TO RUN: SAHAI:

1. docker build -t sahai .
2. docker run -p 8000:8000 --name sahai_backend sahai
3. docker start -a sahai_backend


TO RUN: QRADNT:

1. docker pull qdrant/qdrant
2. docker run -p 6333:6333 -p 6334:6334 -v "$(pwd)/qdrant_storage:/qdrant/storage:z" qdrant/qdrant


You can then send requests after both of these services are up!