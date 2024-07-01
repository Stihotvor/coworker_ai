import random
import string
from typing import cast

import redis
from fastapi import FastAPI, HTTPException

app = FastAPI()


# Create healthcheck endpoint
@app.get("/healthcheck/")
def healthcheck():
    return {"status": "ok"}


@app.get("/test_redis")
def test_redis():
    try:
        r = redis.Redis(host='redis', port=6379, db=0)
        r.ping()
        return {"message": "Connected to Redis successfully!"}
    except redis.exceptions.ConnectionError:
        raise HTTPException(status_code=500, detail="Unable to connect to Redis")

