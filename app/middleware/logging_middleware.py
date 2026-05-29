"""Logging Middleware"""

import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import AppLogger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging all requests"""

    def __init__(self, app):
        super().__init__(app)
        self.logger = AppLogger("http")

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        start_time = time.time()

        # Log request
        self.logger.info(
            f"Request: {request.method} {request.url.path}",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            clien=request.client.host if request.client else "unknown",
        )

        try:
            response = await call_next(request)
            process_time = time.time() - start_time

            # Log response
            self.logger.info(
                f"Response: {response.status_code}",
                request_id=request_id,
                status_code=response.status_code,
                duration_ms=round(process_time * 1000, 2),
            )

            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)

            return response
        except Exception as e:
            self.logger.error(f"Error: {str(e)}", request_id=request_id, error=str(e))
            raise
