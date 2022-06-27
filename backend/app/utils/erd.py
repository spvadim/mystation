from loguru import logger
from pysnmp.hlapi.asyncio import *

from ..db.engine import engine
from ..db.system_settings import get_system_settings

erd_logger = logger.bind(name="erd")
on = Integer(1)
off = Integer(0)


def preob_numb(ports_used: str):
    number = 0
    for i in ports_used:
        if i == "0":
            number = 0
        else:
            number += 2 ** (int(i) - 1)
    return number


async def snmp_set(
    community_string,
    ip_address_host,
    port_snmp,
    key,
    value,
    lookup_mib,
    engine=SnmpEngine(),
    context=ContextData(),
):
    return await setCmd(
        engine,
        CommunityData(community_string),
        UdpTransportTarget((ip_address_host, port_snmp)),
        context,
        ObjectType(ObjectIdentity(key), value),
        lookupMib=lookup_mib,
    )


async def snmp_set_yellow_on():
    erd_logger.info("Включение желтого цвета на колонне")

    current_settings = await get_system_settings()
    if current_settings.general_settings.use_owen.value:
        lookup_mib = False
        owen_settings = current_settings.owen_settings
        community_string = owen_settings.owen_community_string.value
        port_snmp = owen_settings.owen_snmp_port.value
        ip_address_host = owen_settings.owen_ip.value
        oid = owen_settings.owen_oid.value
        yellow_port = owen_settings.owen_yellow_port.value
        owen_ports_used = owen_settings.owen_ports_used.value
        if not yellow_port in owen_ports_used:
            owen_ports_used += yellow_port
            current_settings.owen_settings.owen_ports_used.value = owen_ports_used
            await engine.save(current_settings)
        value = Unsigned32(preob_numb(owen_ports_used))
    else:
        lookup_mib = True
        value = on
        erd_settings = current_settings.erd_settings
        community_string = erd_settings.erd_community_string.value
        port_snmp = erd_settings.erd_snmp_port.value
        ip_address_host = erd_settings.erd_ip.value
        oid = erd_settings.erd_yellow_oid.value
    await snmp_set(community_string, ip_address_host, port_snmp, oid, value, lookup_mib)


async def snmp_set_yellow_off():
    erd_logger.info("Выключение желтого цвета на колонне")

    current_settings = await get_system_settings()
    if current_settings.general_settings.use_owen.value:
        lookup_mib = False
        owen_settings = current_settings.owen_settings
        community_string = owen_settings.owen_community_string.value
        port_snmp = owen_settings.owen_snmp_port.value
        ip_address_host = owen_settings.owen_ip.value
        oid = owen_settings.owen_oid.value
        yellow_port = owen_settings.owen_yellow_port.value
        owen_ports_used = owen_settings.owen_ports_used.value
        owen_ports_used = owen_ports_used.replace(yellow_port, "")
        current_settings.owen_settings.owen_ports_used.value = owen_ports_used
        await engine.save(current_settings)
        value = Unsigned32(preob_numb(owen_ports_used))
    else:
        lookup_mib = True
        value = off
        erd_settings = current_settings.erd_settings
        community_string = erd_settings.erd_community_string.value
        port_snmp = erd_settings.erd_snmp_port.value
        ip_address_host = erd_settings.erd_ip.value
        oid = erd_settings.erd_yellow_oid.value
    await snmp_set(community_string, ip_address_host, port_snmp, oid, value, lookup_mib)


async def snmp_set_red_on():
    erd_logger.info("Включение красного цвета на колонне")

    current_settings = await get_system_settings()
    if current_settings.general_settings.use_owen.value:
        lookup_mib = False
        owen_settings = current_settings.owen_settings
        community_string = owen_settings.owen_community_string.value
        port_snmp = owen_settings.owen_snmp_port.value
        ip_address_host = owen_settings.owen_ip.value
        oid = owen_settings.owen_oid.value
        red_port = owen_settings.owen_red_port.value
        owen_ports_used = owen_settings.owen_ports_used.value
        if not red_port in owen_ports_used:
            owen_ports_used += red_port
            current_settings.owen_settings.owen_ports_used.value = owen_ports_used
            await engine.save(current_settings)
        value = Unsigned32(preob_numb(owen_ports_used))
    else:
        lookup_mib = True
        value = on
        erd_settings = current_settings.erd_settings
        community_string = erd_settings.erd_community_string.value
        port_snmp = erd_settings.erd_snmp_port.value
        ip_address_host = erd_settings.erd_ip.value
        oid = erd_settings.erd_red_oid.value
    await snmp_set(community_string, ip_address_host, port_snmp, oid, value, lookup_mib)


async def snmp_set_red_off():
    erd_logger.info("Выключение красного цвета на колонне")

    current_settings = await get_system_settings()
    if current_settings.general_settings.use_owen.value:
        lookup_mib = False
        owen_settings = current_settings.owen_settings
        community_string = owen_settings.owen_community_string.value
        port_snmp = owen_settings.owen_snmp_port.value
        ip_address_host = owen_settings.owen_ip.value
        oid = owen_settings.owen_oid.value
        red_port = owen_settings.owen_red_port.value
        owen_ports_used = owen_settings.owen_ports_used.value
        owen_ports_used = owen_ports_used.replace(red_port, "")
        current_settings.owen_settings.owen_ports_used.value = owen_ports_used
        await engine.save(current_settings)
        value = Unsigned32(preob_numb(owen_ports_used))
    else:
        lookup_mib = True
        value = off
        erd_settings = current_settings.erd_settings
        community_string = erd_settings.erd_community_string.value
        port_snmp = erd_settings.erd_snmp_port.value
        ip_address_host = erd_settings.erd_ip.value
        oid = erd_settings.erd_red_oid.value
    await snmp_set(community_string, ip_address_host, port_snmp, oid, value, lookup_mib)


async def snmp_set_green_on():
    erd_logger.info("Включение зеленого цвета на колонне")

    current_settings = await get_system_settings()
    if current_settings.general_settings.use_owen.value:
        lookup_mib = False
        owen_settings = current_settings.owen_settings
        community_string = owen_settings.owen_community_string.value
        port_snmp = owen_settings.owen_snmp_port.value
        ip_address_host = owen_settings.owen_ip.value
        oid = owen_settings.owen_oid.value
        green_port = owen_settings.owen_green_port.value
        owen_ports_used = owen_settings.owen_ports_used.value
        if not green_port in owen_ports_used:
            owen_ports_used += green_port
            current_settings.owen_settings.owen_ports_used.value = owen_ports_used
            await engine.save(current_settings)
        value = Unsigned32(preob_numb(owen_ports_used))
    else:
        lookup_mib = True
        value = on
        erd_settings = current_settings.erd_settings
        community_string = erd_settings.erd_community_string.value
        port_snmp = erd_settings.erd_snmp_port.value
        ip_address_host = erd_settings.erd_ip.value
        oid = erd_settings.erd_green_oid.value
    await snmp_set(community_string, ip_address_host, port_snmp, oid, value, lookup_mib)


async def snmp_set_green_off():
    erd_logger.info("Выключение зеленого цвета на колонне")

    current_settings = await get_system_settings()
    if current_settings.general_settings.use_owen.value:
        lookup_mib = False
        owen_settings = current_settings.owen_settings
        community_string = owen_settings.owen_community_string.value
        port_snmp = owen_settings.owen_snmp_port.value
        ip_address_host = owen_settings.owen_ip.value
        oid = owen_settings.owen_oid.value
        green_port = owen_settings.owen_green_port.value
        owen_ports_used = owen_settings.owen_ports_used.value
        owen_ports_used = owen_ports_used.replace(green_port, "")
        current_settings.owen_settings.owen_ports_used.value = owen_ports_used
        await engine.save(current_settings)
        value = Unsigned32(preob_numb(owen_ports_used))
    else:
        lookup_mib = True
        value = off
        erd_settings = current_settings.erd_settings
        community_string = erd_settings.erd_community_string.value
        port_snmp = erd_settings.erd_snmp_port.value
        ip_address_host = erd_settings.erd_ip.value
        oid = erd_settings.erd_green_oid.value
    await snmp_set(community_string, ip_address_host, port_snmp, oid, value, lookup_mib)


async def snmp_set_buzzer_on():
    erd_logger.info("Включение зуммера")

    current_settings = await get_system_settings()
    if current_settings.general_settings.use_owen.value:
        lookup_mib = False
        owen_settings = current_settings.owen_settings
        community_string = owen_settings.owen_community_string.value
        port_snmp = owen_settings.owen_snmp_port.value
        ip_address_host = owen_settings.owen_ip.value
        oid = owen_settings.owen_oid.value
        buzzer_port = owen_settings.owen_buzzer_port.value
        owen_ports_used = owen_settings.owen_ports_used.value
        if not buzzer_port in owen_ports_used:
            owen_ports_used += buzzer_port
            current_settings.owen_settings.owen_ports_used.value = owen_ports_used
            await engine.save(current_settings)
        value = Unsigned32(preob_numb(owen_ports_used))
    else:
        lookup_mib = True
        value = on
        erd_settings = current_settings.erd_settings
        community_string = erd_settings.erd_community_string.value
        port_snmp = erd_settings.erd_snmp_port.value
        ip_address_host = erd_settings.erd_ip.value
        oid = erd_settings.erd_buzzer_oid.value
    await snmp_set(community_string, ip_address_host, port_snmp, oid, value, lookup_mib)


async def snmp_set_buzzer_off():
    erd_logger.info("Выключение зуммера")

    current_settings = await get_system_settings()
    if current_settings.general_settings.use_owen.value:
        lookup_mib = False
        owen_settings = current_settings.owen_settings
        community_string = owen_settings.owen_community_string.value
        port_snmp = owen_settings.owen_snmp_port.value
        ip_address_host = owen_settings.owen_ip.value
        oid = owen_settings.owen_oid.value
        buzzer_port = owen_settings.owen_buzzer_port.value
        owen_ports_used = owen_settings.owen_ports_used.value
        owen_ports_used = owen_ports_used.replace(buzzer_port, "")
        current_settings.owen_settings.owen_ports_used.value = owen_ports_used
        await engine.save(current_settings)
        value = Unsigned32(preob_numb(owen_ports_used))
    else:
        lookup_mib = True
        value = off
        erd_settings = current_settings.erd_settings
        community_string = erd_settings.erd_community_string.value
        port_snmp = erd_settings.erd_snmp_port.value
        ip_address_host = erd_settings.erd_ip.value
        oid = erd_settings.erd_buzzer_oid.value
    await snmp_set(community_string, ip_address_host, port_snmp, oid, value, lookup_mib)


async def snmp_raise_damper():
    erd_logger.info("Подъем шторки")

    lookup_mib = True
    current_settings = await get_system_settings()
    erd_settings = current_settings.second_erd_settings
    community_string = erd_settings.erd_community_string.value
    port_snmp = erd_settings.erd_snmp_port.value
    ip_address_host = erd_settings.erd_ip.value
    first_oid = erd_settings.erd_first_oid.value
    await snmp_set(
        community_string, ip_address_host, port_snmp, first_oid, on, lookup_mib
    )


async def snmp_finish_damper():
    erd_logger.info("Опускание шторки")

    lookup_mib = True
    current_settings = await get_system_settings()
    erd_settings = current_settings.second_erd_settings
    community_string = erd_settings.erd_community_string.value
    port_snmp = erd_settings.erd_snmp_port.value
    ip_address_host = erd_settings.erd_ip.value
    first_oid = erd_settings.erd_first_oid.value
    await snmp_set(
        community_string, ip_address_host, port_snmp, first_oid, off, lookup_mib
    )


async def snmp_raise_ejector():
    erd_logger.info("Подъем сбрасывателя")

    lookup_mib = True
    current_settings = await get_system_settings()
    erd_settings = current_settings.second_erd_settings
    community_string = erd_settings.erd_community_string.value
    port_snmp = erd_settings.erd_snmp_port.value
    ip_address_host = erd_settings.erd_ip.value
    second_oid = erd_settings.erd_second_oid.value
    await snmp_set(
        community_string, ip_address_host, port_snmp, second_oid, on, lookup_mib
    )


async def snmp_finish_ejector():
    erd_logger.info("Опускание сбрасывателя")

    lookup_mib = True
    current_settings = await get_system_settings()
    erd_settings = current_settings.second_erd_settings
    community_string = erd_settings.erd_community_string.value
    port_snmp = erd_settings.erd_snmp_port.value
    ip_address_host = erd_settings.erd_ip.value
    second_oid = erd_settings.erd_second_oid.value
    await snmp_set(
        community_string, ip_address_host, port_snmp, second_oid, off, lookup_mib
    )


async def snmp_third_erd_first_oid_on():
    erd_logger.info("on signal on first oid")

    lookup_mib = True
    current_settings = await get_system_settings()
    erd_settings = current_settings.third_erd_settings
    community_string = erd_settings.erd_community_string.value
    port_snmp = erd_settings.erd_snmp_port.value
    ip_address_host = erd_settings.erd_ip.value
    first_oid = erd_settings.erd_first_oid.value
    await snmp_set(
        community_string, ip_address_host, port_snmp, first_oid, on, lookup_mib
    )


async def snmp_third_erd_first_oid_off():
    erd_logger.info("off signal on first oid")

    lookup_mib = True
    current_settings = await get_system_settings()
    erd_settings = current_settings.third_erd_settings
    community_string = erd_settings.erd_community_string.value
    port_snmp = erd_settings.erd_snmp_port.value
    ip_address_host = erd_settings.erd_ip.value
    first_oid = erd_settings.erd_first_oid.value
    await snmp_set(
        community_string, ip_address_host, port_snmp, first_oid, off, lookup_mib
    )
