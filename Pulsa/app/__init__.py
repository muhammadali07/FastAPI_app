from fastapi import FastAPI
from mongoengine import connect
from starlette.testclient import TestClient

from app.routers import users, todos

app = FastAPI()

mongodb = connect('mongodb', host='mongodb://localhost/pulsa')
client = TestClient(app)

app.include_router(users.router, prefix="/users", tags=["User Docs"], )
app.include_router(users.router, prefix="/todo", tags=["Todo Docs!"], )
