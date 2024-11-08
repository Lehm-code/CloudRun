from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/")
async def read_root(request: Request):
    data = await request.json()
    last_name = data.get("lastName")
    first_name = data.get("firstName")
    if last_name and first_name:
        return {"message": f"Hello, {last_name} {first_name}! from FastAPI"}
    else:
        return {"message": "Hello, World! from FastAPI"}
