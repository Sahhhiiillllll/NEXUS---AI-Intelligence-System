"""
J.A.R.V.I.S — Vercel Serverless API
====================================
FastAPI backend that runs automatically on Vercel when the app is deployed.
No separate server process needed — the API starts with every request.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from intents import IntentRouter
from logger import get_logger

log = get_logger("api_index")

app = FastAPI(
    title="J.A.R.V.I.S API",
    description="Serverless backend for J.A.R.V.I.S — auto-runs on Vercel",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = IntentRouter()


class QueryRequest(BaseModel):
    text: str


async def _process_chat(text: str) -> dict:
    log.info(f"API received query: {text[:60]}")
    result = await router.route(text)
    result["type"] = "response"
    return result


@app.post("/api/chat")
@app.post("/chat")
async def chat_endpoint(request: QueryRequest):
    try:
        return await _process_chat(request.text)
    except Exception as e:
        log.error(f"API routing error: {e}")
        return {
            "response": "I encountered an unexpected error. Please try again.",
            "tool": "llm",
            "log": f"Error: {str(e)[:80]}",
            "type": "response",
        }


@app.get("/api/health")
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "J.A.R.V.I.S API is online.",
        "mode": "serverless",
    }

@app.get("/api/debug_fs")
async def debug_fs():
    import os
    
    debug_info = {
        "cwd": os.getcwd(),
        "file_dir": os.path.dirname(os.path.abspath(__file__)),
    }
    
    try:
        # Walk current working directory safely
        cwd_files = []
        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                cwd_files.append(os.path.join(root, file))
        debug_info["cwd_tree"] = cwd_files[:200] # limit to 200 to avoid huge output
    except Exception as e:
        debug_info["cwd_tree_error"] = str(e)
        
    try:
        # Walk __file__ directory safely
        file_dir_files = []
        for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__))):
            for file in files:
                file_dir_files.append(os.path.join(root, file))
        debug_info["file_dir_tree"] = file_dir_files[:200]
    except Exception as e:
        debug_info["file_dir_tree_error"] = str(e)
        
    return debug_info

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# We'll use a dynamic finder for the public directory
public_dir = None
for p in [
    os.path.join(os.getcwd(), "api", "public"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "public"),
    os.path.join(os.getcwd(), "public"),
]:
    if os.path.exists(p) and os.path.isdir(p):
        public_dir = p
        break

@app.get("/")
async def serve_index():
    if public_dir:
        index_path = os.path.join(public_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
    return {"detail": "Frontend index.html not found", "public_dir_found": public_dir}

if public_dir:
    app.mount("/", StaticFiles(directory=public_dir), name="static")
