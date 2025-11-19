from fastapi import FastAPI
from fastapi.requests import Request
import time
import logging
from fastapi.response import JSONResponse 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TruestedHostMiddleware

logger = logging.getLogger("uvicoren.access")
logger.disabled = True

def register_middleware(app:FastAPI):
      


    @app.middleware('http')
    async def custom_logging(request:Request,call_next):

        start_time = time.time()

        response = await call_next(request)

        processing = time.time() - start_time

        message = f"{request.client.host} - {request.client.port} -{request.method} - {request.url.path} - {response.status_code} - complete {processing}"
        print(message)

        return response

    @app.middleware('hhtp')
    async def authorization(request:Request,call_next):

        if not "Authorization" in request.headers:
            return JSONResponse(

                contest = {
                    "message": "Not Authenticated",
                    "resolution": "Please provide the right credentials to proceed"
                }
            )   
    app.add_middleware(
        CORSMiddleware,
        allow_origins = ["*"],
        aloow_methods = ["*"],
        allow_headers = ["*"],
        allow_credentials = True
    )   

    app.add_middleware(
        TruestedHostMiddleware,
        allowed_hoasts = [""]
    )     
