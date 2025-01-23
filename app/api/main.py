from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from ..services.model_manager import ModelManager
from ..services.file_manager import FileManager

app = FastAPI()
file_manager = FileManager()
model_manager = ModelManager(file_manager)

class ModelRequest(BaseModel):
    name: str
    code: str

class TrainRequest(BaseModel):
    name: str
    data: Dict[str, Any]

@app.post("/api/models")
async def create_model(request: ModelRequest):
    try:
        path = model_manager.create_model(request.name, request.code)
        return {"message": "Model created successfully", "path": path}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/models")
async def list_models():
    try:
        models = file_manager.list_models()
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/train")
async def train_model(request: TrainRequest):
    try:
        result = model_manager.train_model(request.name, request.data)
        return {"message": "Model trained successfully", "result": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 