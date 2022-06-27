import logging
import sys
from pprint import pformat

from loguru import logger


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentaion.
    """

    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def format_record(record: dict) -> str:
    """
    Custom format for loguru loggers.
    Uses pformat for log any data like request/response body during debug.
    Works with logging if loguru handler it.
    """

    format_string = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS UTCZ}</> | "
        "<level>{level: <8}</> | "
        "<yellow>PID={process:02d}</> | "
        "<cyan>{name}:{function}:{line}</> - "
        "<level>{message}</>"
    )

    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"],
            indent=4,
            compact=True,
            width=88,
        )
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"
    return format_string


def make_filter(name: str) -> callable:
    def filter(record):
        return record["extra"].get("name") == name

    return filter


def init_logging():
    """
    Replaces logging handlers with a handler for using the custom handler.
    WARNING!
    if you call the init_logging in startup event function,
    then the first logs before the application start will be in the old format
    """

    # disable handlers for specific uvicorn loggers
    # to redirect their output to the default uvicorn logger
    intercept_handler = InterceptHandler()
    loggers = (
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn.")
    )
    for uvicorn_logger in loggers:
        uvicorn_logger.handlers = [intercept_handler]

    # change handler for default uvicorn logger
    logging.getLogger("uvicorn").handlers = [intercept_handler]

    # set logs output, level and format
    logger.configure(
        handlers=[
            dict(
                sink=sys.stdout,
                level=logging.DEBUG,
                format=format_record,
                enqueue=True,
            ),
            dict(
                sink="logs/deep_logs.log",
                level=logging.DEBUG,
                format=format_record,
                filter=make_filter("deep"),
                enqueue=True,
            ),
            dict(
                sink="logs/light_logs.log",
                level=logging.DEBUG,
                format=format_record,
                filter=make_filter("light"),
                enqueue=True,
            ),
            dict(
                sink="logs/wdiot_logs.log",
                level=logging.DEBUG,
                format=format_record,
                filter=make_filter("wdiot"),
                enqueue=True,
            ),
            dict(
                sink="logs/erd_logs.log",
                level=logging.DEBUG,
                format=format_record,
                filter=make_filter("erd"),
                enqueue=True,
            ),
            dict(
                sink="logs/tg_logs.log",
                level=logging.DEBUG,
                format=format_record,
                filter=make_filter("tg"),
                enqueue=True,
            ),
            dict(
                sink="logs/email_logs.log",
                level=logging.DEBUG,
                format=format_record,
                filter=make_filter("email"),
                enqueue=True,
            ),
        ]
    )
