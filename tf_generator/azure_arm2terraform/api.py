import os

import aiofiles
from fastapi import APIRouter, Request

from tf_generator.utils.utils import extract_folder

router = APIRouter()

@router.post("/upload")
async def transform_az2tf(request: Request):
    try:
        filename = request.headers['filename']
        async with aiofiles.open(os.path.join("data", filename), 'wb+') as f:
            async for chunk in request.stream():
                await f.write(chunk)
        extract_folder(os.path.join("data", filename))
    except Exception:
        return {"message": "There was an error uploading the file"}

    return {"message": f"Successfully uploaded {filename}"}