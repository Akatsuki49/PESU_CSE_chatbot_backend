# Sahai and Qdrant Setup Instructions

This document outlines the steps to set up and run the Sahai backend and Qdrant vector database, including using a Python virtual environment.

## Prerequisites

* Docker installed on your system.
* Python 3.x installed on your system.
* `add_data.py` script in the same directory as your `Dockerfile`.
* `QA.xlsx` file should be present in the same file directory.

## Sahai Setup (with Python Virtual Environment)

1.  **Create and Activate Virtual Environment:**

    * Navigate to the directory containing your `Dockerfile` and `add_data.py`.
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

2.  **Install Dependencies (if any):**

    * If your `add_data.py` script has dependencies, install them using pip:

        ```bash
        pip install -r requirements.txt #if you have a requirements.txt file
        # or
        pip install package1 package2 # if you install packages manually
        ```

3.  **Add Data (Python Script):**

    * Run the `add_data.py` Python script to preprocess and prepare your data:

        ```bash
        python add_data.py
        ```

4.  **Deactivate Virtual Environment (Optional):**

    * After the script is finished, you can deactivate the virtual environment:

        ```bash
        deactivate
        ```

5.  **Build Docker Image:**

    * Build the Docker image for the Sahai backend:

        ```bash
        docker build -t sahai .
        ```

6.  **Run Docker Container:**

    * Run the Sahai backend container, mapping port 8000:

        ```bash
        docker run -p 8000:8000 --name sahai_backend sahai
        ```

7.  **Attach to Running Container (Optional):**

    * If you stopped the container and want to reattach to it's logs.
    * Start the container.

        ```bash
        docker start sahai_backend
        ```
    * Attach to the container's output.

        ```bash
        docker attach sahai_backend
        ```

## Qdrant Setup

1.  **Pull Qdrant Image:**

    * Pull the Qdrant Docker image:

        ```bash
        docker pull qdrant/qdrant
        ```

2.  **Run Qdrant Container:**

    * Run the Qdrant container, mapping ports 6333 and 6334, and mounting a volume for storage:

        ```bash
        docker run -p 6333:6333 -p 6334:6334 -v "$(pwd)/qdrant_storage:/qdrant/storage:z" qdrant/qdrant
        ```

## Sending Requests

Once both the Sahai and Qdrant containers are running, you can send requests to the Sahai backend on port 8000. Ensure that Qdrant is also running so that Sahai can properly utilize the vector database.