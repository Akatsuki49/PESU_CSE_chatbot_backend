# Sahai and Qdrant Setup Instructions (Docker Compose)

This document outlines the steps to set up and run the Sahai backend and Qdrant vector database using Docker Compose.

## Prerequisites

* Docker and Docker Compose installed on your system.
* `add_data.py` script in the same directory as your `Dockerfile` and `docker-compose.yml`.
* `QA.xlsx` file should be present in the same file directory.
* A `docker-compose.yml` file configured to run both the Sahai and Qdrant services.

## Docker Compose Setup

1.  **Run Docker Compose:**

    * Ensure you are in the directory containing the `docker-compose.yml` file, `Dockerfile`, `add_data.py`, and `QA.xlsx`.
    * Run the following command to build and start the Sahai and Qdrant containers:

        ```bash
        docker-compose up --build
        ```

2.  **Wait for Service Startup:**

    * After running the `docker-compose up --build` command, wait until you see the following message in your terminal logs:

        ```
        backend_service | INFO:     Uvicorn running on [http://0.0.0.0:8000](http://0.0.0.0:8000) (Press CTRL+C to quit)
        ```

    * This message indicates that the Sahai backend service has started successfully and is ready to receive requests.

## Sending Requests

Once the Sahai backend service is running, you can send requests to it on port 8000. Ensure that Qdrant is also running so that Sahai can properly utilize the vector database.

**Sending a Query:**

Send a `POST` request to the following endpoint, replacing `"user question"` with your actual query:

```
http://localhost:8000/query?query="user question"
```