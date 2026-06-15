"""Logging Middleware"""

import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging all requests"""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        start_time = time.time()

        logger.info(
            f"Request {request_id}: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )

        try:
            response = await call_next(request)
            process_time = time.time() - start_time

            logger.info(
                f"Response {request_id}: {response.status_code} "
                f"in {round(process_time * 1000, 2)}ms"
            )

            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)
            return response

        except Exception as e:
            logger.error(f"Error {request_id}: {str(e)}")
            raise
