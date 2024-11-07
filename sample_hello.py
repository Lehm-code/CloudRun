from fastapi import FastAPI
from typing import Optional
# from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# # CORSの設定
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # 必要に応じて許可するオリジンを指定
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.get("/")
def read_root(last_name: Optional[str] = None, first_name: Optional[str] = None):
    if last_name and first_name:
        return {"message": f"Hello, {last_name} {first_name}! from FastAPI"}
    else:
        return {"message": "Hello, World! from FastAPI"}
