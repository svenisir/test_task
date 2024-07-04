import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.config import settings
from app.logger import logger
from app.memes.open.router import router as open_router
from app.memes.private.router import router as private_router
from app.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(settings.REDIS_URL,
                              decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(
    lifespan=lifespan
)

app.include_router(users_router)
app.include_router(open_router)
app.include_router(private_router)

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Authorization"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request execution time", extra={
        "process_time": round(process_time, 4)
    })
    return response
