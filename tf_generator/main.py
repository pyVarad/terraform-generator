import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

from tf_generator.core.logging_config import configure_logging
from tf_generator.routes.ct2tf.end_points import ct2tf_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Bootstrapping th application.")
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(ct2tf_router, prefix="/cloudformation2terraform")

@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} - {exc.detail}")
    return await http_exception_handler(request, exc)