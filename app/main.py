from fastapi import FastAPI
from app.api.v1.message_routes import router
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from app.errors import BaseError


app = FastAPI()
app.include_router(router)


@app.exception_handler(BaseError)
async def base_error_handler(request: Request, exc: BaseError):

    return JSONResponse(
        status_code=exc.status,
        content={"detail": exc.text},
    )
