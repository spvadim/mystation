import snap7
from loguru import logger

from ..models.system_settings.pintset_settings import PintsetSettings


wdiot_logger = logger.bind(name="wdiot")


def off_pintset(settings: PintsetSettings) -> bool:
    wdiot_logger.info("Выключение пинцета")
    try:
        plc = snap7.client.Client()
        ip = settings.pintset_ip.value
        wdiot_logger.info(f"Ip: {ip}")
        rack = settings.pintset_rack.value
        wdiot_logger.info(f"Rack: {rack}")
        slot = settings.pintset_slot.value
        wdiot_logger.info(f"Slot: {slot}")
        tcpport = settings.pintset_tcp_port.value
        wdiot_logger.info(f"tcp port: {tcpport}")
        wdiot_logger.info("Пытаюсь подключится к plc")
        plc.connect(ip, rack, slot, tcpport)
        wdiot_logger.info("Подключился к plc")

        db_name = settings.pintset_db_name.value
        wdiot_logger.info(f"db_name: {db_name}")
        starting_byte = settings.pintset_starting_byte.value
        wdiot_logger.info(f"starting_byte: {starting_byte}")
        length = settings.pintset_reading_length.value
        wdiot_logger.info(f"length: {length}")
        reading = plc.db_read(db_name, starting_byte, length)
        wdiot_logger.info(f"reading: {reading}")

        byte_number = settings.pintset_byte_number.value
        wdiot_logger.info(f"Byte_number: {byte_number}")
        bit_number = settings.pintset_bit_number.value
        wdiot_logger.info(f"Bit_number: {bit_number}")
        pintset_turning_off_value = settings.pintset_turning_off_value.value
        wdiot_logger.info(f"Pintset_turning_off_value: {pintset_turning_off_value}")
        wdiot_logger.info("Пытаюсь выполнить set_bool")
        snap7.util.set_bool(reading, byte_number, bit_number, pintset_turning_off_value)
        wdiot_logger.info("Выполнил set_bool")

        wdiot_logger.info(f"reading: {reading}")
        wdiot_logger.info("Пытаюсь выполнить db_write")
        plc.db_write(db_name, starting_byte, reading)
        wdiot_logger.info("Выполнил db_write")
        wdiot_logger.info("Пытаюсь отключится от plc")
        plc.disconnect()
        wdiot_logger.info("Отключился от plc")
        plc.destroy()

    except snap7.exceptions.Snap7Exception as e:
        wdiot_logger.info(f"Ошибка во время выключения пинцета: {e}")
        return False
    wdiot_logger.info("Пинцет выключен")
    return True


def on_pintset(settings: PintsetSettings) -> bool:
    wdiot_logger.info("Включение пинцета")
    try:
        plc = snap7.client.Client()
        ip = settings.pintset_ip.value
        wdiot_logger.info(f"Ip: {ip}")
        rack = settings.pintset_rack.value
        wdiot_logger.info(f"Rack: {rack}")
        slot = settings.pintset_slot.value
        wdiot_logger.info(f"Slot: {slot}")
        tcpport = settings.pintset_tcp_port.value
        wdiot_logger.info(f"tcp port: {tcpport}")
        wdiot_logger.info("Пытаюсь подключится к plc")
        plc.connect(ip, rack, slot, tcpport)
        wdiot_logger.info("Подключился к plc")

        db_name = settings.pintset_db_name.value
        wdiot_logger.info(f"db_name: {db_name}")
        starting_byte = settings.pintset_starting_byte.value
        wdiot_logger.info(f"starting_byte: {starting_byte}")
        length = settings.pintset_reading_length.value
        wdiot_logger.info(f"length: {length}")
        reading = plc.db_read(db_name, starting_byte, length)
        wdiot_logger.info(f"reading: {reading}")

        byte_number = settings.pintset_byte_number.value
        wdiot_logger.info(f"Byte_number: {byte_number}")
        bit_number = settings.pintset_bit_number.value
        wdiot_logger.info(f"Bit_number: {bit_number}")
        pintset_turning_on_value = settings.pintset_turning_on_value.value
        wdiot_logger.info(f"Pintset_turning_on_value: {pintset_turning_on_value}")
        wdiot_logger.info("Пытаюсь выполнить set_bool")
        snap7.util.set_bool(reading, byte_number, bit_number, pintset_turning_on_value)
        wdiot_logger.info("Выполнил set_bool")

        wdiot_logger.info(f"reading: {reading}")
        wdiot_logger.info("Пытаюсь выполнить db_write")
        plc.db_write(db_name, starting_byte, reading)
        wdiot_logger.info("Выполнил db_write")
        wdiot_logger.info("Пытаюсь отключится от plc")
        plc.disconnect()
        wdiot_logger.info("Отключился от plc")
        plc.destroy()

    except snap7.exceptions.Snap7Exception as e:
        wdiot_logger.info(f"Ошибка во время включения пинцета: {e}")
        return False
    wdiot_logger.info("Пинцет включен")
    return True


def drop_pack_ejector(settings: PintsetSettings) -> bool:
    wdiot_logger.info("Cброс пачки за пинцетом")
    try:
        plc = snap7.client.Client()
        ip = settings.pintset_ip.value
        wdiot_logger.info(f"Ip: {ip}")
        rack = settings.pintset_rack.value
        wdiot_logger.info(f"Rack: {rack}")
        slot = settings.pintset_slot.value
        wdiot_logger.info(f"Slot: {slot}")
        tcpport = settings.pintset_tcp_port.value
        wdiot_logger.info(f"tcp port: {tcpport}")
        wdiot_logger.info("Пытаюсь подключится к plc")
        plc.connect(ip, rack, slot, tcpport)
        wdiot_logger.info("Подключился к plc")

        db_name = settings.pintset_db_name.value
        wdiot_logger.info(f"db_name: {db_name}")
        starting_byte = settings.ejector_starting_byte.value
        wdiot_logger.info(f"starting_byte: {starting_byte}")
        length = settings.ejector_reading_length.value
        wdiot_logger.info(f"length: {length}")
        reading = plc.db_read(db_name, starting_byte, length)
        wdiot_logger.info(f"reading: {reading}")

        byte_number = settings.ejector_byte_number.value
        wdiot_logger.info(f"Byte_number: {byte_number}")
        bit_number = settings.ejector_bit_number.value
        wdiot_logger.info(f"Bit_number: {bit_number}")
        ejector_drop_value = settings.ejector_drop_value.value
        wdiot_logger.info(f"ejector_drop_value: {ejector_drop_value}")
        wdiot_logger.info("Пытаюсь выполнить set_bool")
        snap7.util.set_bool(reading, byte_number, bit_number, ejector_drop_value)
        wdiot_logger.info("Выполнил set_bool")

        wdiot_logger.info(f"reading: {reading}")
        wdiot_logger.info("Пытаюсь выполнить db_write")
        plc.db_write(db_name, starting_byte, reading)
        wdiot_logger.info("Выполнил db_write")
        wdiot_logger.info("Пытаюсь отключится от plc")
        plc.disconnect()
        wdiot_logger.info("Отключился от plc")
        plc.destroy()

    except snap7.exceptions.Snap7Exception as e:
        wdiot_logger.info(f"Ошибка во время выключения пинцета: {e}")
        return False
    wdiot_logger.info("Пачка сброшена")
    return True
