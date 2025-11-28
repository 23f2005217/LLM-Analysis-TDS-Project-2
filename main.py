from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agent import run_agent
from dotenv import load_dotenv
import uvicorn
import os
import time
from logger import setup_logger

load_dotenv()

logger = setup_logger("main")

EMAIL = os.getenv("EMAIL") 
SECRET = os.getenv("SECRET")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
START_TIME = time.time()
@app.get("/healthz")
def healthz():
    return {
        "status": "ok",
        "uptime_seconds": int(time.time() - START_TIME)
    }

@app.post("/solve")
async def solve(request: Request, background_tasks: BackgroundTasks):
    try:
        data = await request.json()
    except Exception as e:
        logger.error(f"JSON parse error: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    if not data:
        logger.error("Empty data received")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    url = data.get("url")
    secret = data.get("secret")
    if not url or not secret:
        logger.error("Missing url or secret")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    if secret != SECRET:
        logger.warning(f"Invalid secret provided: {secret}")
        raise HTTPException(status_code=403, detail="Invalid secret")
    logger.info(f"Verified starting the task for URL: {url}")
    background_tasks.add_task(run_agent, url)

    return JSONResponse(status_code=200, content={"status": "ok"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)