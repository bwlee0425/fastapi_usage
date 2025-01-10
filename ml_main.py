from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pickle

app = FastAPI()

# 모델 로드, iris_model.pkl : 코랩에서 T4-gpu 를 이용해 생성
with open("iris_model.pkl", "rb") as f:
    model = pickle.load(f)

class IrisModel(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

target_names=['setosa', 'versicolor', 'virginica']

@app.post("/predict")
def predict_iris(iris: IrisModel):
    data = np.array([[iris.sepal_length, iris.sepal_width, iris.petal_length, iris.petal_width]])
    prediction = model.predict(data)
    return {"prediction": target_names[int(prediction[0])]}