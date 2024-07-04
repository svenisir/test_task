from contextlib import asynccontextmanager

from aiobotocore.session import get_session
from fastapi import UploadFile

from app.config import settings


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, file: UploadFile, key: str):
        async with self.get_client() as client:
            file_data = await file.read()
            await client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=file_data,
            )
            await file.close()

    async def delete_file(self, key: str):
        async with self.get_client() as client:
            await client.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )


s3_client = S3Client(
    access_key=settings.ACCESS_KEY,
    secret_key=settings.SECRET_KEY,
    endpoint_url=settings.ENDPOINT_URL,
    bucket_name=settings.BUCKET_NAME
)
