import os

from celery import Celery

app = Celery(
    'blog',
    broker=os.getenv("RABBITMQ_URL", "amqp://Dora:Noviigod1!@rabbitmq:5672/"),
    backend='rpc://',
    include=['src.tasks']
)

app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
app.conf.accept_content = ["json"]
app.conf.timezone = "UTC"
