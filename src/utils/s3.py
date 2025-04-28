import uuid
from io import BytesIO

from fastapi import UploadFile
from minio import Minio

from src.core.config import settings

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)

BUCKET_NAME = "images"

def ensure_bucket():
    if not minio_client.bucket_exists(BUCKET_NAME):
        minio_client.make_bucket(BUCKET_NAME)

async def upload_image(file: UploadFile):
    try:
        ensure_bucket()
        file_name = f"{uuid.uuid4()}_{file.filename}"
        content = await file.read()  # Получаем байты
        if not content:
            raise ValueError("Empty image file")
        # Передаем байты как BytesIO для MinIO
        minio_client.put_object(
            BUCKET_NAME,
            file_name,
            data=BytesIO(content),
            length=len(content),
            content_type=file.content_type
        )
        return f"http://{settings.MINIO_ENDPOINT}/{BUCKET_NAME}/{file_name}"
    except Exception as e:
        raise Exception(f"Failed to upload image: {str(e)}")
