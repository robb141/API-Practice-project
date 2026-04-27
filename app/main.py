from fastapi import FastAPI

from app.routes import router


# Create the FastAPI application object.
# This object is what Uvicorn imports and runs.
app = FastAPI(title="Task API")

# Register all endpoint routes from app/routes.py.
app.include_router(router)
