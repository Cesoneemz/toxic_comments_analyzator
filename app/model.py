import torch

from transformers import pipeline
from transformers import AutoTokenizer, AutoModel, AutoConfig, BatchEncoding

from typing import List, Dict, Any

pipe = pipeline('feature-extraction', model='DeepPavlov/rubert-base-cased')

tokenizer = None
model = None
config = None

classifier = None

labels: List[str] = ["not toxic", "toxic"]

def load_model():
    global tokenizer, model, classifier
    tokenizer = AutoTokenizer.from_pretrained("DeepPavlov/rubert-base-cased")
    model = AutoModel.from_pretrained("DeepPavlov/rubert-base-cased")
    config = AutoConfig.from_pretrained("DeepPavlov/rubert-base-cased")
    classifier = torch.nn.Linear(config.hidden_size, 2)

def tokenize_text(text: str) -> BatchEncoding:
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=128)
    return inputs

def predict_toxity(text: str) -> Dict[str, Any]:
    inputs = tokenize_text(text)
    with torch.no_grad():
        outputs = model(**inputs)
    last_hidden_state = outputs.last_hidden_state
    logits = classifier(last_hidden_state[:, 0, :])
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    predicted_class = torch.argmax(probabilities, dim=-1).item()
    return {"label": labels[predicted_class], "confidence": probabilities[0][predicted_class].item()}
