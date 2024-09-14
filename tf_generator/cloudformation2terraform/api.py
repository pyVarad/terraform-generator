import os
import shutil
import subprocess
import uuid
from logging import basicConfig

import aiofiles
from fastapi import APIRouter, Request
from starlette.responses import FileResponse
from starlette.background import BackgroundTask

from tf_generator.utils.utils import extract_folder, get_files_and_folders_recursively, zip_folder

router = APIRouter()

def cleanup(temp_file: str):
    os.remove(temp_file)

@router.post("/upload")
async def transform_ct2tf(request: Request):
    data_dir = os.path.join("data")
    try:
        temp_dir = str(uuid.uuid4())
        if not os.path.isdir(os.path.join(data_dir, temp_dir)):
            os.mkdir(os.path.join(data_dir, temp_dir))
        filename = request.headers['filename']
        async with aiofiles.open(os.path.join(data_dir, temp_dir, filename), 'wb') as f:
            async for chunk in request.stream():
                await f.write(chunk)
        extract_folder(os.path.join(data_dir, temp_dir, filename), os.path.join(data_dir, temp_dir))
        sub_directories, files = get_files_and_folders_recursively(os.path.join(data_dir, temp_dir, filename.split(".")[0]))
        target = os.path.join(data_dir, temp_dir, "random")
        for file in files:
            subprocess.run(["cf2tf", file, "-o", os.path.join(target, os.path.basename(file).split(".")[0])])
        zip_folder(os.path.join(data_dir, "random.zip"), target)
        shutil.rmtree(os.path.join(data_dir, temp_dir), ignore_errors=True)
    except Exception as e:
        print(e)
        response = {"message": "There was an error uploading the file"}

    return FileResponse(
            os.path.join(data_dir, "random.zip"),
            background=BackgroundTask(cleanup, os.path.join(data_dir, "random.zip"))
        )