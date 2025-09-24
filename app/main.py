from fastapi import FastAPI
from app.api.v1.message_routes import router as msg_router
from app.api.v1.database_test import router as db_router
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from app.errors import BaseError
from databases import Database

app = FastAPI()
app.include_router(msg_router)
app.include_router(db_router)


@app.exception_handler(BaseError)
async def base_error_handler(request: Request, exc: BaseError):

    return JSONResponse(
        status_code=exc.status,
        content={"detail": exc.text},
    )
