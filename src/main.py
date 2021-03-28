from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.api import api_router

app = FastAPI(title="spotter")


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception) -> Any:
    error_message = f"Unexpected error occurred: {exc}"
    return JSONResponse(status_code=500, content={"detail": error_message})


app.include_router(api_router, prefix="/bot")
