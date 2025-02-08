from fastapi import FastAPI, UploadFile, HTTPException, WebSocket, WebSocketDisconnect
import shutil
from rag import call_llm, retrieve_ans
from store import store_xl, store_single_qa
from websocketManager import ConnectionManager
from getSimilarQuestions import getSimilarQuestions
import json

app = FastAPI()
manager = ConnectionManager()

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
    
# @app.post("/upload_single_qa/")
# async def upload_single_qa(question: str, answer: str):
#     try:
#         store_single_qa(question, answer)
#         return {"message": "Question and answer stored successfully."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/communicate")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Received:{data}",websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.websocket("/upload_single_qa/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if "question" in data and "answer" in data:
                question = data["question"]
                answer = data["answer"]
                similar_data = getSimilarQuestions(question)
                similar_qna = []
                for data in similar_data:
                    qna = {
                            "question": data.payload["question"],
                            "answer": data.payload["answer"]
                        }
                    similar_qna.append(qna)
                
                qna_json = json.dumps(similar_qna)
                await manager.send_personal_message(f"Similar questions and answers:",websocket)
                await manager.send_personal_message(qna_json,websocket)
            else:
                if "confirm" in data:
                    store_single_qa(question, answer)
                    await manager.send_personal_message(f"Data stored successfully",websocket)
                manager.disconnect(websocket)


    except WebSocketDisconnect:
        manager.disconnect(websocket)

# fastapi run main.py --host 0.0.0.0 --port 8000 : not used now
# fastapi dev main.py --reload

# docker run -p 6333:6333 -p 6334:6334 `
#      -v "${PWD}/qdrant_storage:/qdrant/storage" `
#      --name qdrant_VDB `              
#  qdrant/qdrant