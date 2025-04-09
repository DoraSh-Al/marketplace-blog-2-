from minio import Minio

from src.core.config import settings

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)

def upload_image(file):
    bucket_name = "images"
    # Проверяем, существует ли бакет, и создаём, если нет
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
    minio_client.put_object(
        bucket_name,
        file.filename,
        file.file,
        length=-1,
        part_size=10*1024*1024
    )
    return f"http://{settings.MINIO_ENDPOINT}/{bucket_name}/{file.filename}"
