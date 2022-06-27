from typing import List

from fastapi import APIRouter, Depends, HTTPException
from odmantic import ObjectId

from ..db.events import add_events, get_event_by_id, get_events, mark_event_processed
from ..models.event import Event, EventFilters, EventInput, EventOutput, EventsOutput
from .custom_routers import DeepLoggerRoute, LightLoggerRoute

deep_logger_router = APIRouter(route_class=DeepLoggerRoute)
light_logger_router = APIRouter(route_class=LightLoggerRoute)


@light_logger_router.get("/events", response_model=EventsOutput)
async def list_events(filters: EventFilters = Depends()) -> EventsOutput:
    return await get_events(filters=filters)


@deep_logger_router.put("/events", response_model=List[EventOutput])
async def add_event(event: EventInput) -> List[Event]:
    if not event.camera_number:
        camera_numbers = []
    else:
        camera_numbers = [event.camera_number]
    return await add_events(
        event.event_type, event.message, camera_numbers=camera_numbers
    )


@deep_logger_router.patch("/events/{id}", response_model=EventOutput)
async def process_event(id: ObjectId) -> Event:
    return await mark_event_processed(id)


@light_logger_router.get("/events/{id}", response_model=EventOutput)
async def get_event(id: ObjectId) -> Event:
    event = await get_event_by_id(id)
    if not event:
        raise HTTPException(404, f"Ивент с id={id} не найден!")

    return event
