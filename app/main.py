from fastapi import FastAPI

app = FastAPI()

@app.get("/")

def read_root():

    return {"mensaje": "backend de wilito funcionandoooo"}