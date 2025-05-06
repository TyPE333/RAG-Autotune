from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import uvicorn


app = FastAPI()

@app.get("/health")
async def health():
    """
    Health check endpoint for the application.

    Returns:
        dict: A dictionary containing the status of the application.
    """
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)