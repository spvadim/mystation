import asyncio
import inspect
from datetime import datetime
from time import sleep

from loguru import logger

from ..db.db_utils import (
    delete_packs_under_pintset,
    flush_packing_table,
    flush_pintset,
    flush_state,
    get_current_state,
    packing_table_error,
    pintset_error,
    pintset_withdrawal_error,
    set_column_red,
    set_column_yellow,
    sync_error,
)
from ..db.engine import pymongo_db as db
from ..db.events import add_events
from ..db.system_settings import get_system_settings
from ..models.event import Event
from ..models.system_settings.pintset_settings import PintsetSettings
from ..models.system_settings.erd_settings import SignalSettings
from .email import send_email
from .erd import (
    snmp_finish_damper,
    snmp_finish_ejector,
    snmp_raise_damper,
    snmp_raise_ejector,
    snmp_set_buzzer_off,
    snmp_set_buzzer_on,
    snmp_set_green_off,
    snmp_set_green_on,
    snmp_set_red_off,
    snmp_set_red_on,
    snmp_set_yellow_off,
    snmp_set_yellow_on,
    snmp_third_erd_first_oid_off,
    snmp_third_erd_first_oid_on,
)
from .pintset import drop_pack_ejector, off_pintset, on_pintset

wdiot_logger = logger.bind(name="wdiot")


async def send_error():
    await snmp_set_green_off()
    await snmp_set_red_on()


async def send_error_with_buzzer():
    await send_error()
    await snmp_set_buzzer_on()


async def send_warning():
    await snmp_set_green_off()
    await snmp_set_yellow_on()


async def flush_to_normal():
    await snmp_set_buzzer_off()
    await snmp_set_yellow_off()
    await snmp_set_red_off()
    await snmp_set_green_on()


async def send_warning_and_back_to_normal(delay: int, message: str):
    tasks_before_sleep = [
        send_warning(),
        set_column_yellow(message),
    ]

    await asyncio.gather(*tasks_before_sleep)
    await asyncio.sleep(delay)

    state = await get_current_state()
    if state.error_msg == message:
        tasks_after_sleep = [
            flush_state(),
            flush_to_normal(),
        ]
        await asyncio.gather(*tasks_after_sleep)


async def drop_pack_ejector_erd(message: str, second_erd_settings):
    delay_before_damper = second_erd_settings.delay_before_damper.value
    delay_before_ejector = second_erd_settings.delay_before_ejector.value
    delay_after_ejector = second_erd_settings.delay_after_ejector.value

    await asyncio.sleep(delay_before_damper)
    await snmp_raise_damper()

    await asyncio.sleep(delay_before_ejector)
    await snmp_raise_ejector()

    await asyncio.sleep(delay_after_ejector)
    tasks_after_ejector = [
        snmp_finish_ejector(),
        snmp_finish_damper(),
        add_events("error", message),
    ]
    await asyncio.gather(*tasks_after_ejector)


def drop_pack_ejector_snap7(
    error_msg: str, pintset_settings: PintsetSettings, current_datetime: datetime
):
    drop_pack_ejector(pintset_settings)
    event = Event(time=current_datetime, message=error_msg, event_type="error")
    db.event.insert_one(event.dict())


def drop_pack_after_pintset_snap7(
    error_msg: str,
    pintset_settings: PintsetSettings,
    current_datetime: datetime,
    use_additional_event: bool,
):

    sleep(pintset_settings.pintset_delay_before_freezing.value)
    wdiot_logger.info("Заморозил пинцет")
    off_pintset(pintset_settings)

    wdiot_logger.info("Взвел ошибку на пинцете")
    db.system_status.find_one_and_update(
        {},
        {
            "$set": {
                "system_state.pintset_state": "error",
                "system_state.pintset_error_msg": error_msg,
            }
        },
    )
    event = Event(time=current_datetime, message=error_msg, event_type="error")
    db.event.insert_one(event.dict())
    if not use_additional_event:
        packs_to_delete = db.pack.find({"status": "под пинцетом", "in_queue": True})
        deleted_qrs = ", ".join([pack["qr"] for pack in packs_to_delete])
        db.pack.delete_many({"status": "под пинцетом", "in_queue": True})
        wdiot_logger.info(f"Удалил пачки с такими qr кодами: {deleted_qrs}")

    delay = pintset_settings.pintset_curtain_opening_duration.value
    sleep(delay)

    if db.system_status.find_one({})["system_state"]["pintset_error_msg"] == error_msg:
        wdiot_logger.info("Убираю ошибку на пинцете")
        db.system_status.find_one_and_update(
            {},
            {
                "$set": {
                    "system_state.pintset_state": "normal",
                    "system_state.pintset_error_msg": None,
                }
            },
        )
        if delay > 0:
            wdiot_logger.info("Разморозил пинцет")
            on_pintset(pintset_settings)


async def drop_pack_after_pintset_erd(
    error_msg: str, pintset_settings: PintsetSettings, use_additional_event: bool
):
    await asyncio.sleep(pintset_settings.pintset_delay_before_freezing.value)
    wdiot_logger.info("Заморозил пинцет")
    await snmp_third_erd_first_oid_on()

    wdiot_logger.info("Взвел ошибку на пинцете")
    await pintset_error(error_msg)

    if not use_additional_event:
        deleted_packs = await delete_packs_under_pintset()
        deleted_qrs = ", ".join([pack.qr for pack in deleted_packs])
        wdiot_logger.info(f"Удалил пачки с такими qr кодами: {deleted_qrs}")

    delay = pintset_settings.pintset_curtain_opening_duration.value
    await asyncio.sleep(delay)

    state = await get_current_state()
    if state.pintset_error_msg == error_msg:
        wdiot_logger.info("Убираю ошибку на пинцете")
        await flush_pintset()
        wdiot_logger.info("Разморозил пинцет")
        await snmp_third_erd_first_oid_off()


async def turn_default_error(message: str):
    tasks = []
    tasks.append(set_column_red(message))
    tasks.append(send_error())
    results = await asyncio.gather(*tasks)
    return results[0]


async def turn_default_warning(message: str):
    tasks = []
    tasks.append(set_column_yellow(message))
    tasks.append(send_warning())
    results = await asyncio.gather(*tasks)
    return results[0]


async def flush_default_state():
    tasks = []
    tasks.append(flush_state())
    tasks.append(flush_to_normal())
    results = await asyncio.gather(*tasks)
    return results[0]


async def turn_packing_table_error(message: str, cube_id):
    tasks = []
    tasks.append(packing_table_error(message, cube_id))
    tasks.append(send_error_with_buzzer())
    email_message = f"<br> {message}."
    tasks.append(send_email("Ошибка на упаковочном столе", email_message))
    wdiot_logger.error(message)
    results = await asyncio.gather(*tasks)
    return results[0]


async def flush_packing_table_error():
    tasks = []
    tasks.append(flush_packing_table())
    tasks.append(flush_to_normal())
    results = await asyncio.gather(*tasks)
    return results[0]


async def turn_sync_error(method_name: str, message: str):
    current_settings = await get_system_settings()
    tasks = []
    email_message = f"<br> {message}."
    if current_settings.general_settings.sync_request.value:
        email_message += "<br> Перевел синхронизацию в статус ERROR."
        tasks.append(sync_error(message))
        tasks.append(send_error_with_buzzer())
        if current_settings.general_settings.sync_raise_damper.value:
            tasks.append(snmp_raise_damper())

    tasks.append(send_email(f"Рассинхрон в {method_name}", email_message))

    results = await asyncio.gather(*tasks)
    wdiot_logger.error(message)
    return results[0]


async def add_sync_error_to_bg_tasks(background_tasks, message: str):
    method_name = inspect.stack()[1].function
    background_tasks.add_task(turn_sync_error, method_name, message)


async def add_send_email_to_bg_tasks(background_tasks, title: str, email_body: str):
    method_name = inspect.stack()[1].function
    title += f" в {method_name}"
    background_tasks.add_task(send_email, title, email_body)


async def turn_sync_fixing():
    tasks = [
        snmp_set_buzzer_off(),
    ]
    await asyncio.gather(*tasks)


async def flush_sync_to_normal():
    tasks = [
        flush_to_normal(),
        snmp_finish_damper(),
    ]

    await asyncio.gather(*tasks)


async def turn_pintset_withdrawal_error(message: str):
    tasks = [
        pintset_withdrawal_error(message),
        send_error_with_buzzer(),
    ]
    email_message = f"<br> {message}."
    tasks.append(send_email("Выемка из под пинцета", email_message))
    wdiot_logger.error(message)
    results = await asyncio.gather(*tasks)
    return results[0]


async def add_cube_qr(signal_settings: SignalSettings):
    await snmp_set_buzzer_on()
    qr_added_time = datetime.now()
    duration = signal_settings.add_qr_to_cube_signal_duration.value
    while (datetime.now() - qr_added_time).seconds < duration:
        await snmp_set_green_off()
        await snmp_set_yellow_on()
        await snmp_set_green_on()
        await snmp_set_yellow_off()

    await snmp_set_buzzer_off()


async def drop_signal(signal_settings: SignalSettings):
    duration = signal_settings.drop_signal_duration.value
    await send_error_with_buzzer()
    await asyncio.sleep(duration)
    await flush_to_normal()
