"""RFC 7807 compliant problem details error responses."""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


def register_error_handlers(app):
    """Register custom exception handlers compliant with RFC 7807."""

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        headers = getattr(exc, "headers", None) or {}
        headers["Content-Type"] = "application/problem+json"
        payload = {
            "type": f"https://httpstatuses.com/{exc.status_code}",
            "title": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "status": exc.status_code,
            "detail": exc.detail if isinstance(exc.detail, str) else str(exc.detail),
            "instance": str(request.url.path)
        }
        return JSONResponse(status_code=exc.status_code, content=payload, headers=headers)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        payload = {
            "type": "https://httpstatuses.com/422",
            "title": "Unprocessable Entity (Validation Error)",
            "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "detail": str(exc.errors()),
            "instance": str(request.url.path)
        }
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=payload,
            headers={"Content-Type": "application/problem+json"}
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        payload = {
            "type": "https://httpstatuses.com/500",
            "title": "Internal Server Error",
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "detail": "An internal unexpected error occurred. Please consult the error instance log.",
            "instance": str(request.url.path)
        }
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=payload,
            headers={"Content-Type": "application/problem+json"}
        )
