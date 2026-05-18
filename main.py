from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Prueba Técnica OneMillionCopy, realizada por Anderson Sepulveda"}