import logging
import os
import shutil
import subprocess
import uuid
from typing import Annotated

import aiofiles
from fastapi import APIRouter, Request, Header, status as http_status
from starlette.background import BackgroundTask
from starlette.responses import FileResponse, Response

from tf_generator.utils.utils import extract_folder, get_files_and_folders_recursively, zip_folder

router = APIRouter()
logger = logging.getLogger(__name__)

def cleanup(temp_dir: str):
    logger.info(f"Clean up {temp_dir} folder")
    shutil.rmtree(os.path.join(temp_dir), ignore_errors=True)

@router.post("/upload",     openapi_extra={
        "requestBody": {
            "content": {
            "multipart/form-data": {
              "schema": {
                "type": "object",
                "properties": {
                  "file": {
                    "type": "string",
                    "format": "binary",
                    "description": "The file to upload"
                  }
                },
                "required": ["file"]
              }
            }
          }
        }
    },)
async def transform_ct2tf(
        request: Request,
        filename: Annotated[str, Header()],
        response: Response
):
    data_dir = os.path.join("data")
    try:
        temp_dir = str(uuid.uuid4())
        response.headers["Content-Type"] = "application/zip"
        os.mkdir(os.path.join(data_dir, temp_dir))
        logger.info(f"Started processing the uploaded {filename}")
        async with aiofiles.open(os.path.join(data_dir, temp_dir, filename), 'wb') as f:
            async for chunk in request.stream():
                await f.write(chunk)
        extract_folder(os.path.join(data_dir, temp_dir, filename), os.path.join(data_dir, temp_dir))
        sub_directories, files = get_files_and_folders_recursively(
            os.path.join(data_dir, temp_dir, filename.split(".")[0])
        )
        target = os.path.join(data_dir, temp_dir, "random")
        for file in files:
            subprocess.run(
                ["cf2tf", file, "-o", os.path.join(target, os.path.basename(file).split(".")[0])]
            )
        logger.info(f"Completed processing successfully")
        zip_folder(os.path.join(data_dir, temp_dir, "random.zip"), target)
    except Exception as e:
        logger.error(f"Failed with exception message {e}")
        response.headers["Content-Type"] = "application/json"
        return {"message": "There was an error uploading the file"}, 500

    return FileResponse(
            os.path.join(data_dir, temp_dir, "random.zip"),
            media_type="application/octet-stream",
            status_code=http_status.HTTP_201_CREATED,
            filename=f"terraform-{temp_dir}.zip",
            background=BackgroundTask(cleanup, os.path.join(data_dir, temp_dir))
        )