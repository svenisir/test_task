from fastapi import APIRouter, UploadFile, Depends, Response, status
from aiobotocore.client import UnknownServiceError

from app.storage import s3_client
from app.users.dependencies import get_current_user
from app.memes.dao import MemDAO
from app.memes.schemas import SMem
from app.exceptions import CannotAddMemException, CannotDeleteMemException, CannotUpdateMemException
from app.logger import logger


router = APIRouter(
    prefix="/memes",
    tags=["Работа с мемами"],
    dependencies=[Depends(get_current_user)]
)


@router.post("")
async def add_new_mem(
        file: UploadFile,
        description: str,
) -> int:
    # get id of the added record
    mem_id = await MemDAO.add(description=description, file_name=file.filename)

    try:
        # trying to add a picture to minio
        await s3_client.upload_file(file, f"{mem_id}_{file.filename}")
    except UnknownServiceError:
        # if any exception, delete record by id and returning exception
        await MemDAO.delete_by_id(mem_id)
        raise CannotAddMemException

    return mem_id


@router.put("/{mem_id}")
async def update_mem(
        mem_id: int,
        description: str,
        file: UploadFile,
) -> None:
    # get updated mem
    old_mem = await MemDAO.get_by_id(model_id=mem_id)
    await MemDAO.update(model_id=mem_id, file_name=file.filename, description=description)

    try:
        # trying load new file to minio
        await s3_client.upload_file(file, f"{mem_id}_{file.filename}")
        logger.info("Successful update")
    except UnknownServiceError:
        # if any exception occurs, we restore the old data
        await MemDAO.update(model_id=mem_id,
                            file_name=old_mem.file_name,
                            description=old_mem.description)
        raise CannotUpdateMemException

    # delete the old file from minio if successful
    await s3_client.delete_file(key=f"{old_mem.id}_{old_mem.file_name}")


@router.delete("/{mem_id}")
async def delete_me(
        response: Response,
        mem_id: int,
) -> SMem:
    # get a delete mem
    mem = await MemDAO.delete_by_id(model_id=mem_id)

    try:
        # trying delete mem from minio
        await s3_client.delete_file(key=f"{mem.id}_{mem.file_name}")
        response.status_code = status.HTTP_204_NO_CONTENT
    except UnknownServiceError:
        # if any exception, add delete mem in db
        await MemDAO.add(description=mem.description, file_name=mem.file_name)
        raise CannotDeleteMemException

    return mem


