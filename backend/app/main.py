from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import auth, settings
from app.core.config import get_settings
from app.core.errors import AppError
from app.schemas.common import fail, ok

app = FastAPI(title="Egg Distribution Management System", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in get_settings().cors_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppError)
async def app_error_handler(_: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content=fail(exc.code, exc.message))


@app.exception_handler(RequestValidationError)
async def validation_error_handler(_: Request, exc: RequestValidationError):
    first = exc.errors()[0]
    where = ".".join(str(p) for p in first["loc"] if p != "body")
    return JSONResponse(
        status_code=422, content=fail("VALIDATION_ERROR", f"{where}: {first['msg']}")
    )


@app.get("/api/v1/health", tags=["health"])
def health():
    return ok({"status": "up"})


app.include_router(auth.router, prefix="/api/v1")
app.include_router(settings.router, prefix="/api/v1")
