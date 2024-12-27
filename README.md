TO RUN: SAHAI:

1. docker build -t sahai .
2. docker run -p 8000:8000 --name sahai_backend sahai
3. docker start -a sahai_backend
