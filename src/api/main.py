import logging

import redis
from fastapi import FastAPI, HTTPException

from src.settings import init_settings

log = logging.getLogger("apiLogger.main")

app = FastAPI()

init_settings()


# Create healthcheck endpoint
@app.get("/healthcheck/")
def healthcheck():
    log.debug("Healthcheck endpoint hit")
    return {"status": "ok"}


@app.get("/healthcheck-redis/")
def test_redis():
    log.debug("Redis connection test endpoint hit")
    try:
        r = redis.Redis(host='redis', port=6379, db=0)
        r.ping()
        return {"status": "ok"}
    except redis.exceptions.ConnectionError:
        raise HTTPException(status_code=500, detail="Unable to connect to Redis")
