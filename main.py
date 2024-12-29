from fastapi import FastAPI, UploadFile, HTTPException
import shutil
from rag import call_llm, retrieve_ans
from store import store_xl, store_single_qa

app = FastAPI()

@app.post("/query/")
async def query_pipeline(query: str):
    try:
        relevant_ans = retrieve_ans(query)
        final_ans = call_llm(query, relevant_ans)
        return {"query": query, "relevant_doc": relevant_ans, "final_response": final_ans}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload_file/")
async def upload_data(file: UploadFile):
    if file.filename.endswith(".xlsx"):
        try:
            temp_file_path = f"temp_{file.filename}"
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Call the store_xl function with the file path
            store_xl(temp_file_path)

            return {"message": f"File {file.filename} uploaded and processed successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Only .xlsx files are supported.")
    
@app.post("/upload_single_qa/")
async def upload_single_qa(question: str, answer: str):
    try:
        store_single_qa(question, answer)
        return {"message": "Question and answer stored successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# fastapi run main.py --host 0.0.0.0 --port 8000