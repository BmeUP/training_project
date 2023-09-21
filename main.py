from fastapi import FastAPI

from src.db.main import Base, engine
from src.users.main import user_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(user_router)