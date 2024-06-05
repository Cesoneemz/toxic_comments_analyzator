FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir fastapi uvicorn joblib catboost pandas scikit-learn nltk

COPY . .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]