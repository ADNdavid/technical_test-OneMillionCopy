from fastapi import FastAPI
from app.routers import leads
from db import create_all_tables

app = FastAPI(lifespan=create_all_tables)
app.include_router(leads.router)

@app.get("/")
async def root():
    return {"message": "Prueba Técnica OneMillionCopy, realizada por Anderson Sepulveda"}