from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:Noviigod1!@localhost:5433/blog_db"
    SECRET_KEY: str = "esowRE3mlGTOK3DnTCx839-uI9EmB3-t6IAvuRDTZ6-kb9ru4z-bF_r_JYCtDAaP72o"
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "Dora"
    MINIO_SECRET_KEY: str = "Noviigod1!"
    RABBITMQ_URL: str = "amqp://Dora:Noviigod1!@localhost:5672/"
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587  # Порт как int
    SMTP_USER: str = "dasasiraeva882@gmail.com"
    SMTP_PASSWORD: str = "fmhnkstlczbromxe"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
