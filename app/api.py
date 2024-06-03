from fastapi import FastAPI, Request
from pydantic import BaseModel

from app.model import predict_toxity, load_model

app = FastAPI()

class PredictionRequest(BaseModel):
    text: str 

class PredictionResponse(BaseModel):
    label: str
    confidence: float

@app.on_event("startup")
async def startup_event():
    load_model()

@app.post("/predict/", response_model=PredictionResponse)
async def predict(request: PredictionRequest) -> PredictionResponse:
    prediction = predict_toxity(request.text)
    return PredictionResponse(**prediction)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)