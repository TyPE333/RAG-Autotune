from fastapi import FastAPI
from app.api.ask import router as ask_router
from app.api.health import router as health_router
from app.api.feedback import router as feedback_router

import uvicorn

app = FastAPI()
app.include_router(ask_router)
app.include_router(health_router)
app.include_router(feedback_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)