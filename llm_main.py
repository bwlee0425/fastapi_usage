from fastapi import FastAPI
from pydantic import BaseModel
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch

# Hugging Face DistilBERT base model (uncased)
app = FastAPI()
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

class TextData(BaseModel):
    text: str

@app.post("/classify/")
async def classify_text(data: TextData):
    inputs = tokenizer(data.text, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits

        predicted_class_id = logits.argmax().item()
        model.config.id2label[predicted_class_id]
    output = ["부정","긍정"]
    print("result", output[predicted_class_id])
    return {"result": predicted_class_id}