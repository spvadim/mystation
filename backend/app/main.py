from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

from .db.db_utils import create_status_if_not_exists
from .db.engine import models_startup
from .db.system_settings import create_system_settings_if_not_exists
from .logger import init_logging
from .routers import (
    cameras,
    cubes,
    events,
    multipacks,
    packs,
    pintset_tasks,
    production_batches,
    system_settings,
    system_status,
)

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url="/api/v1_0/openapi.json",
)
app.include_router(
    production_batches.deep_logger_router, tags=["batches_frontend"], prefix="/api/v1_0"
)
app.include_router(
    production_batches.light_logger_router,
    tags=["batches_frontend"],
    prefix="/api/v1_0",
)
app.include_router(
    packs.deep_logger_router, tags=["packs_frontend"], prefix="/api/v1_0"
)
app.include_router(
    packs.light_logger_router, tags=["packs_frontend"], prefix="/api/v1_0"
)
app.include_router(
    multipacks.deep_logger_router, tags=["multipacks_frontend"], prefix="/api/v1_0"
)
app.include_router(
    multipacks.light_logger_router, tags=["multipacks_frontend"], prefix="/api/v1_0"
)
app.include_router(
    cubes.deep_logger_router, tags=["cubes_frontend"], prefix="/api/v1_0"
)
app.include_router(
    cubes.light_logger_router, tags=["cubes_frontend"], prefix="/api/v1_0"
)
app.include_router(
    system_status.deep_logger_router, tags=["state_and_mode"], prefix="/api/v1_0"
)
app.include_router(
    system_status.light_logger_router, tags=["state_and_mode"], prefix="/api/v1_0"
)
app.include_router(cameras.deep_logger_router, tags=["camera"], prefix="/api/v1_0")
app.include_router(cameras.light_logger_router, tags=["camera"], prefix="/api/v1_0")
app.include_router(
    system_settings.deep_logger_router, tags=["system_settings"], prefix="/api/v1_0"
)
app.include_router(
    system_settings.light_logger_router, tags=["system_settings"], prefix="/api/v1_0"
)
app.include_router(events.deep_logger_router, tags=["events"], prefix="/api/v1_0")
app.include_router(events.light_logger_router, tags=["events"], prefix="/api/v1_0")
app.include_router(
    pintset_tasks.light_logger_router, tags=["pintset_tasks"], prefix="/api/v1_0"
)


@app.get("/api/v1_0/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/swagger-static/swagger-ui-bundle.js",
        swagger_css_url="/swagger-static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    init_logging()
    await create_status_if_not_exists()
    await create_system_settings_if_not_exists()
    await models_startup()
