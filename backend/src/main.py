from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic_core import PydanticCustomError
from src.core.database import lifespan
from src.api import api_router
from src.core.cors import setup_cors

ERROR_STATUS_MAP = {
    "not_found": 404,
    "unauthorized_error": 401,
    "forbidden_error": 403,
}

app = FastAPI(lifespan=lifespan)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {
            "field": ".".join(str(loc) for loc in err["loc"] if loc != "body"),
            "message": err["msg"].replace("Value error, ", ""),
        }
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={
            "code": "validation_error",
            "message": "Validation failed",
            "errors": errors,
        }
    )

@app.exception_handler(PydanticCustomError)
async def pydantic_custom_error_handler(request: Request, exc: PydanticCustomError):
    status_code = ERROR_STATUS_MAP.get(exc.type, 500)
    return JSONResponse(
        status_code=status_code,
        content={
            "code": exc.type,
            "message": str(exc)
        }
    )

# 未預期錯誤
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "code": "internal_error",
            "message": "Internal server error"
        }
    )
setup_cors(app)
app.include_router(api_router)