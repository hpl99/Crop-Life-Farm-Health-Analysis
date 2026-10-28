"""ETag caching, CORS, and localization middleware."""

import hashlib
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class ETagMiddleware(BaseHTTPMiddleware):
    """Calculates ETag for GET responses and responds with 304 Not Modified if matched."""

    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # Only process successful GET requests with bodies
        if request.method == "GET" and response.status_code == 200:
            body = b"".join([chunk async for chunk in response.body_iterator])
            etag = f'"{hashlib.md5(body).hexdigest()}"'

            client_etag = request.headers.get("if-none-match")
            if client_etag and client_etag.strip() == etag:
                return Response(status_code=304, headers={"ETag": etag, "Cache-Control": "public, max-age=300"})

            # Reconstruct response with etag
            headers = dict(response.headers)
            headers["ETag"] = etag
            headers["Cache-Control"] = "public, max-age=300"
            return Response(content=body, status_code=200, headers=headers, media_type=response.media_type)

        return response


def get_requested_language(accept_language: str = None) -> str:
    """Resolve language: defaults to Marathi ('mr'), supports English ('en')."""
    if not accept_language:
        return "mr"
    al = accept_language.lower()
    if "en" in al and not ("mr" in al and al.index("mr") < al.index("en")):
        return "en"
    return "mr"

