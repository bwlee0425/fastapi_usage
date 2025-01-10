from fastapi import FastAPI, HTTPException
import pandas as pd
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_chroma import Chroma

app = FastAPI()

# 데이터 로드
books = pd.read_excel('science_books.xlsx')

# 임베딩 모델 초기화
sbert = SentenceTransformerEmbeddings(model_name='jhgan/ko-sroberta-multitask')

# 벡터 저장소 생성
vector_store = Chroma.from_texts(
    texts=books['제목'].tolist(),
    embedding=sbert
)

@app.post("/search/")
def search_books(query: str):
    results = vector_store.similarity_search(query=query, k=3)  # 상위 3개 결과 반환
    return {"query": query, "results": results}
