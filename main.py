from fastapi import FastAPI,  HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from authenticator import authenticator
from messages.routers.messages import messages_router
from accounts.routers import accounts
from peers.routers import peers
from matching.routers import matching
from tags.routers import tags
import os
import asyncpg

app = FastAPI()

MAX_CONNECTIONS = 20

@app.on_event("startup")
async def startup():
    try:
        app.state.pool = await asyncpg.create_pool(
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            database=os.getenv("DATABASE_NAME"),
            host=os.getenv("DATABASE_HOST"),
            max_size=MAX_CONNECTIONS
        )
    except asyncpg.exceptions.TooManyConnectionsError:
        raise HTTPException(status_code=503, detail="Service Unavailable")

@app.on_event("shutdown")
async def shutdown():
    await app.state.pool.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.environ.get("CORS_HOST", "http://localhost:3000"),
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(authenticator.router)
app.include_router(accounts.router)
app.include_router(messages_router)
app.include_router(matching.router)
app.include_router(tags.router)
app.include_router(peers.router)

@app.get("/")
def root():
    return {"message": "You hit the root path!"}

@app.get("/api/launch-details")
def launch_details():
    return {
        "launch_details": {
            "module": 3,
            "week": 17,
            "day": 5,
            "hour": 19,
            "min": "00",
        }
    }
