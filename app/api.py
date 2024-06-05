from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib


app = FastAPI()
model = None

model_path = 'catboost_pipeline_gpu.pkl'

class PredictionRequest(BaseModel):
    text: str 

class PredictionResponse(BaseModel):
    text: str
    label: str

@app.on_event("startup")
async def startup_event():
    global model
    try:
        model = joblib.load(model_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Model loading failed")

@app.post("/predict/", response_model=PredictionResponse)
async def predict(request: PredictionRequest) -> PredictionResponse:
    try:
        # Предсказание токсичности комментария
        prediction = model.predict([request.text])
        class_names = ["Not Toxic", "Toxic"]
        result = PredictionResponse(
            text=request.text,
            label=class_names[int(prediction[0])]
        )
        return result
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Prediction failed")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)