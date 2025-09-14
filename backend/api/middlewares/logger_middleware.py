from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
from datetime import datetime
from loguru import logger
from backend.utils.logging import logger_close, logger_setup, logger_setup_file


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        start_time = time.perf_counter()
        date_time = datetime.now()
        request_params = request.query_params

        logger_setup()
        logger_setup_file()

        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        logger.info(f"Request made at {date_time}, with parameters {request_params}, after a duration of {process_time}")

        await logger_close()  # logger_close is asynchronous
        return response
