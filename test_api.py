from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from loguru import logger
from functional import chat_sql

app = FastAPI()


@app.post("/chat")
async def chat(text: str):
    logger.info(f"User: {text}")
    response = chat_sql(question=text)
    return {"response": response}
