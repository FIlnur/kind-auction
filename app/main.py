from fastapi import FastAPI
from app.api.v1.router import api_router
from app.db127.core.config import settings

app = FastAPI(title="My FastAPI Project")

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    # Здесь можно инициализировать подключения, например Redis ping
    pass

@app.on_event("shutdown")
async def shutdown_event():
    from app.db.redis import close_redis
    await close_redis()






    