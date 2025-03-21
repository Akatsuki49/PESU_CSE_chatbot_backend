# Sahai and Qdrant Setup Instructions (Docker Compose)

This document outlines the steps to set up and run the Sahai backend and Qdrant vector database using Docker Compose, including setting up a Python virtual environment.

## Prerequisites

* Docker and Docker Compose installed on your system.
* Python 3.x installed on your system.
* `add_data.py` script in the same directory as your `Dockerfile` and `docker-compose.yml`.
* `QA.xlsx` file should be present in the same file directory.
* A `docker-compose.yml` file configured to run both the Sahai and Qdrant services.
* `requirements.txt` file containing the python dependencies for `add_data.py`.

## Setup Instructions

1.  **Create and Activate Python Virtual Environment:**

    * Navigate to the directory containing your `Dockerfile`, `docker-compose.yml`, `add_data.py`, `QA.xlsx`, and `requirements.txt`.
    * Create a virtual environment:

        ```bash
        python3 -m venv venv
        ```

    * Activate the virtual environment:

        * On Linux/macOS:

            ```bash
            source venv/bin/activate
            ```

        * On Windows:

            ```bash
            venv\Scripts\activate
            ```

    * Install the dependencies from `requirements.txt`:

        ```bash
        pip install -r requirements.txt
        ```


    * If you are appending data to an existing database, run the `md_and_paraphrase.py` script:

        ```bash
        python md_and_paraphrase.py
        ```

    * **Important:** Ensure that if you are appending data, the excel file to be appended is named `original.xlsx`.

2.  **Run Docker Compose in one terminal:**

    * Open another new terminal window.
    * Navigate to the same directory as in step 1.
    * Run the following command to build and start the Sahai and Qdrant containers:

        ```bash
        docker-compose up --build
        ```

3.  **Run `add_data.py` in a separate terminal:**

    * Open a new terminal window.
    * Navigate to the same directory as in step 1.
    * Ensure the virtual environment is activated.
    * Run the `add_data.py` script:

        ```bash
        python add_data.py
        ```

    * **Important:** Execute this only when you see 'qdrant' written in dots in the terminal.


4.  **Wait for Service Startup:**

    * In the Docker Compose terminal window, wait until you see the following message in your logs:

        ```
        backend_service | INFO:     Uvicorn running on [invalid URL removed] (Press CTRL+C to quit)
        ```

    * This message indicates that the Sahai backend service has started successfully and is ready to receive requests.

## Sending Requests

Once the Sahai backend service is running, you can send requests to it on port 8000. Ensure that Qdrant is also running so that Sahai can properly utilize the vector database.

**Sending a Query:**

Send a `POST` request to the following endpoint, replacing `"user question"` with your actual query:

```
http://localhost/query?query="user question"
```