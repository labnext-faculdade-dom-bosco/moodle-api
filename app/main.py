from fastapi import FastAPI

from app.routers import moodle

app = FastAPI(title="Moodle API")

app.include_router(moodle.router)
