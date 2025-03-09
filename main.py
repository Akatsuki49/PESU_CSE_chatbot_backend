from fastapi import FastAPI, UploadFile, HTTPException, WebSocket, WebSocketDisconnect
import shutil
from openpyxl import load_workbook
from pydantic import BaseModel
from io import BytesIO
from rag import call_llm, retrieve_ans, validate
from store import store_xl, store_single_qa
from websocketManager import ConnectionManager
from getSimilarQuestions import getSimilarQuestions, runloop
import json
from typing import List
from delete_points import delete_points

app = FastAPI()
manager = ConnectionManager()

class Question(BaseModel):
    question: str
    answer: str

class QuestionsRequest(BaseModel):
    questions: List[Question]

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
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .xlsx files are supported.")

    try:
        # Read the uploaded file into memory
        contents = await file.read()
        workbook = load_workbook(filename=BytesIO(contents))
        sheet = workbook.active
        results = runloop(sheet)
        return {"message": "File processed successfully", "results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")


@app.post("/add_question")
async def add_question(request: QuestionsRequest):
    try:
        for qa in request.questions:
            store_single_qa(qa.question, qa.answer)
        return {"message": "Questions added to Qdrant successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/upload_single_qa/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    isDelete_thread = False
    gotQnA = False
    try:
        while True:
            data = await websocket.receive_json()
            try:
                if "question" in data and "answer" in data:
                    gotQnA = True
                    question = data["question"]
                    answer = data["answer"]
                    similar_data = getSimilarQuestions(question)
                    similar_qna = []
                    for data in similar_data:
                        qna = {
                                "id": data.id,
                                "question": data.payload["question"],
                                "answer": data.payload["answer"]
                            }
                        similar_qna.append(qna)
                    
                    qna_json = json.dumps(similar_qna)
                    await manager.send_personal_message(f"Similar questions and answers:",websocket)
                    await manager.send_personal_message(qna_json,websocket)
                elif "delete" in data:
                    await manager.send_personal_message(f"Send IDs to delete:",websocket)
                    isDelete_thread = True
                elif isDelete_thread:
                    if "ids" in data:
                        ids = data["ids"]
                        delete_points(ids)
                        isDelete_thread = False
                        await manager.send_personal_message(f"Data deleted successfully;",websocket)
                elif "confirm" in data:
                    if not gotQnA:
                        await manager.send_personal_message(f"No data uploaded",websocket)
                    else:
                        store_single_qa(question, answer)
                        gotQnA = False
                        await manager.send_personal_message(f"Data stored successfully",websocket)
                        manager.disconnect(websocket)
                elif "abort" in data:
                        await manager.send_personal_message(f"No data uploaded",websocket)
                        manager.disconnect(websocket)
            except Exception as e:
                await manager.send_personal_message(f"An error occurred: {str(e)}",websocket)
                isDelete_thread = False
                gotQnA = False
                manager.disconnect(websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)

# fastapi run main.py --host 0.0.0.0 --port 8000 : not used now
# fastapi dev main.py --reload

# docker run -p 6333:6333 -p 6334:6334 `
#      -v "${PWD}/qdrant_storage:/qdrant/storage" `
#      --name qdrant_VDB `              
#  qdrant/qdrant