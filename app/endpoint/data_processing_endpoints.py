from fastapi import APIRouter, UploadFile, File

from app.model.data_processing import UploadResponseModel
from app.services.data_processing import process_data
from app.utilities.logger_util import logger

router = APIRouter()


@router.post("/upload", response_model=UploadResponseModel)
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a json file
    """
    logger.info("------- invoked upload_file() -------")

    # Check if the file is a JSON file
    if not file.filename.endswith(".json"):
        return UploadResponseModel(message="Invalid file type. Please upload a JSON file.")

    # Process the file
    response_message = process_data(file)

    logger.info("------- upload_file() completed -------")
    return UploadResponseModel(message=response_message)
