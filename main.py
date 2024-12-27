from fastapi import FastAPI, UploadFile, HTTPException
# from typing import List
import shutil
from rag import answer_gen  # Example function from rag.py
from store import store_xl  # Example functions from store.py

app = FastAPI()

# Endpoint to process a query using the RAG pipeline
@app.post("/query/")
async def query_pipeline(query: str):
    try:
        result = answer_gen(query)  # Call function from rag.py
        return {"query": query, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to upload and store data
@app.post("/upload_file/")
async def upload_data(file: UploadFile):
    if file.filename.endswith(".xlsx"):
        try:
            # Save the uploaded file temporarily
            temp_file_path = f"temp_{file.filename}"
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Call the store_xl function with the file path
            store_xl(temp_file_path)

            # Return success message
            return {"message": f"File {file.filename} uploaded and processed successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Only .xlsx files are supported.")
    
# @app.post("/upload_question/")
# async def upload_question(question: str):
#     try:

# Endpoint to retrieve stored data
# @app.get("/data/")
# async def get_stored_data():
#     try:
#         data = retrieve_data()  # Call function from store.py
#         return {"data": data}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# uvicorn main:app --host 0.0.0.0 --port 8000
