from fastapi import FastAPI
from app.routes import db_health_checkup,query_runner

app = FastAPI()

app.include_router(db_health_checkup.router)
app.include_router(query_runner.router)