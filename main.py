from fastapi import FastAPI
from app.utilities.logger_util import logger

from app.endpoint import data_processing_endpoints, query_endpoints

app = FastAPI()

app.include_router(data_processing_endpoints.router, prefix="/data", tags=["Data Processing"])
app.include_router(query_endpoints.router, prefix="/llm", tags=["LLM QA"])


@app.get("/")
async def root():
    logger.info("Root endpoint accessed. Welcome to the LLM API!")
    return {"message": "Welcome to the LLM API!. Use /docs to see the API documentation."}
