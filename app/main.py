from fastapi import FastAPI
from mangum import Mangum
from app.routes.users import router as users_router
from app.routes.posts import router as posts_router

app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(posts_router, prefix="/posts", tags=["posts"])


@app.get("/")
def read_root():
    """
    Root endpoint
    """
    return {"message": "Welcome to the API"}


@app.get("/health")
def read_health():
    """
    Health check endpoint
    """
    return {"message": "API is healthy"}


handler = Mangum(app, lifespan="off", api_gateway_base_path="/api/v1")
