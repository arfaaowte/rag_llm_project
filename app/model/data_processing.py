from pydantic import BaseModel, Field, ValidationError
from fastapi import HTTPException, UploadFile, File


class UploadParameters(BaseModel):
    """
    This class defines the parameters to upload the data.
    """
    file: UploadFile = File(...)


def parse_upload_param(
        file: UploadFile = File(..., description="The file to be uploaded.")
):
    try:
        return UploadParameters(
            file=file
        )

    except ValidationError as err:
        raise HTTPException(status_code=400, detail=f"{err}") from err


class UploadResponseModel(BaseModel):
    message: str = Field(..., description="Message indicating the status of the upload.")
