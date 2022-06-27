import os

import snap7
from celery import Celery
from loguru import logger

from .db.engine import pymongo_db as db

app = Celery("celery_app")
app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
app.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)

if os.environ.get("PLC_CONNECT"):
    plc = snap7.client.Client()
    system_settings = db.system_settings.find_one({})
    pintset_settings = system_settings["pintset_settings"]
    logger.info(f"{pintset_settings}")
    ip = pintset_settings["pintset_ip"]["value"]
    rack = pintset_settings["pintset_rack"]["value"]
    slot = pintset_settings["pintset_slot"]["value"]
    tcpport = pintset_settings["pintset_tcp_port"]["value"]

    logger.info(f"ip: {ip}, rack: {rack}, slot: {slot}, tcpport: {tcpport}")
    logger.info("try to connect.....")
    plc.connect(ip, rack, slot, tcpport)
    logger.info("connected")


@app.task(bind=True, name="read_bytes")
def read_bytes(self, params: dict):
    db_name = params["db_name"]
    starting_byte = params["starting_byte"]
    length = params["length"]

    try:
        reading = plc.db_read(db_name, starting_byte, length)
        return list(reading)

    except snap7.exceptions.Snap7Exception as e:
        plc.disconnect()
        plc.connect(ip, rack, slot, tcpport)
        self.retry(countdown=0.001, exc=e, max_retries=1)


@app.task(bind=True, name="write_bytes")
def write_bytes(self, params: dict):

    db_name = params["db_name"]
    starting_byte = params["starting_byte"]
    reading = bytearray(params["reading"])

    try:

        plc.db_write(db_name, starting_byte, reading)
        return "OK"

    except snap7.exceptions.Snap7Exception as e:
        plc.disconnect()
        plc.connect(ip, rack, slot, tcpport)
        self.retry(countdown=0.001, exc=e, max_retries=1)
