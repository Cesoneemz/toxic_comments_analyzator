FROM python:3.12 as builder

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn joblib catboost pandas scikit-learn

COPY . .

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]