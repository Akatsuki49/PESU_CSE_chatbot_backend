# Use the official Python base image for Python 3.12.1
FROM python:3.12.1-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application into the working directory
COPY . .

# Expose the default FastAPI port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
