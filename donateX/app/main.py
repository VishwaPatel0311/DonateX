import sys
import traceback
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

root = logging.getLogger("root")
root.setLevel(logging.INFO)
import settings
from api.api_v1.api import router as api_router

# from utilities.api_logging import logging_dependency

app = FastAPI(
    title="DonateX",
    description="A Charitable Donation System with Phone-based Authentication and Payment Gateway Integration.",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)
app.logger = root

app.include_router(api_router)


@app.get("/ping", include_in_schema=False)
async def ping_server():
    return {"result": "OK"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=settings.WEB_PORT, use_colors=True,
                    log_level=logging.DEBUG, reload=True)
    except Exception as err:
        traceback.print_exc()
        print(f"failed to start server: {err}")
        sys.exit(1)
