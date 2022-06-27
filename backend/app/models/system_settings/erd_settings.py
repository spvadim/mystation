from typing import Optional

from odmantic import EmbeddedModel


class ERDIp(EmbeddedModel):
    title: str = "IP ERD контроллера"
    desc: str = "Введите IP ERD контроллера"
    value: Optional[str]
    value_type: str = "string"


class ERDSNMPPort(EmbeddedModel):
    title: str = "SNMP порт ERD контроллера"
    desc: str = "Введите порт SNMP ERD контроллера"
    value: Optional[int]
    value_type: str = "integer"


class ERDCommunityString(EmbeddedModel):
    title: str = "Строка авторизации ERD контроллера"
    desc: str = "Введите строку авторизации ERD контроллера"
    value: Optional[str]
    value_type: str = "string"


class ERDRedOID(EmbeddedModel):
    title: str = "ID красного цвета в ERD контроллере"
    desc: str = "Введите ID красного цвета"
    value: str
    value_type: str = "string"


class ERDYellowOID(EmbeddedModel):
    title: str = "ID желтого цвета в ERD контроллере"
    desc: str = "Введите ID желтого цвета"
    value: str
    value_type: str = "string"


class ERDGreenOID(EmbeddedModel):
    title: str = "ID зеленого цвета в ERD контроллере"
    desc: str = "Введите ID зеленого цвета"
    value: str
    value_type: str = "string"


class ERDBuzzerOID(EmbeddedModel):
    title: str = "ID зуммера в ERD контроллере"
    desc: str = "Введите ID зуммера"
    value: str
    value_type: str = "string"


class ERDFirstOID(EmbeddedModel):
    title: str = "ID первого порта в ERD контроллере"
    desc: str = "Введите ID порта в ерд контроллере"
    value: Optional[str]
    value_type: str = "string"


class ERDSecondOID(EmbeddedModel):
    title: str = "ID второго в ERD контроллере"
    desc: str = "Введите ID порта в ерд контроллере"
    value: Optional[str]
    value_type: str = "string"


class ERDThirdOID(EmbeddedModel):
    title: str = "ID третьего порта в ERD контроллере"
    desc: str = "Введите ID порта в ерд контроллере"
    value: Optional[str]
    value_type: str = "string"


class ERDFourthOID(EmbeddedModel):
    title: str = "ID четвертого порта в ERD контроллере"
    desc: str = "Введите ID порта в ерд контроллере"
    value: Optional[str]
    value_type: str = "string"


class ERDFifthOID(EmbeddedModel):
    title: str = "ID пятого порта в ERD контроллере"
    desc: str = "Введите ID порта в ерд контроллере"
    value: Optional[str]
    value_type: str = "string"


class DelayBeforeDamper(EmbeddedModel):
    title: str = "Задержка перед поднятием шторки"
    desc: str = "Введите задержку в секундах перед открытием шторки"
    value: float = 1.0
    value_type: str = "float"


class DelayBeforeEjector(EmbeddedModel):
    title: str = "Задержка перед поднятием сбрасывателя"
    desc: str = "Введите задержку в секундах перед поднятием сбрасывателя"
    value: float = 0.3
    value_type: str = "float"


class DelayAfterEjector(EmbeddedModel):
    title: str = "Задержка после поднятия сбрасывателя"
    desc: str = "Введите задержку в секундах после поднятия сбрасывателя"
    value: float = 2
    value_type: str = "float"


class ERDSettings(EmbeddedModel):
    title: str = "Настройки ERD контроллера"
    advanced: bool = True
    erd_ip: ERDIp
    erd_snmp_port: ERDSNMPPort
    erd_community_string: ERDCommunityString
    erd_red_oid: ERDRedOID
    erd_yellow_oid: ERDYellowOID
    erd_green_oid: ERDGreenOID
    erd_buzzer_oid: ERDBuzzerOID
    erd_fifth_oid: ERDFifthOID


class SecondERDSettings(EmbeddedModel):
    title: str = "Настройки второго ERD контроллера"
    advanced: bool = True
    erd_ip: ERDIp
    erd_snmp_port: ERDSNMPPort
    erd_community_string: ERDCommunityString
    erd_first_oid: ERDFirstOID
    erd_second_oid: ERDSecondOID
    erd_third_oid: ERDThirdOID
    erd_fourth_oid: ERDFourthOID
    erd_fifth_oid: ERDFifthOID
    delay_before_damper: DelayBeforeDamper = DelayBeforeDamper()
    delay_before_ejector: DelayBeforeEjector = DelayBeforeEjector()
    delay_after_ejector: DelayAfterEjector = DelayAfterEjector()


class ThirdERDSettings(EmbeddedModel):
    title: str = "Настройки третьего ERD контроллера"
    advanced: bool = True
    erd_ip: ERDIp = ERDIp()
    erd_snmp_port: ERDSNMPPort = ERDSNMPPort()
    erd_community_string: ERDCommunityString = ERDCommunityString()
    erd_first_oid: ERDFirstOID = ERDFirstOID()
    erd_second_oid: ERDSecondOID = ERDSecondOID()
    erd_third_oid: ERDThirdOID = ERDThirdOID()
    erd_fourth_oid: ERDFourthOID = ERDFourthOID()
    erd_fifth_oid: ERDFifthOID = ERDFifthOID()


class OwenGreenPort(EmbeddedModel):
    title: str = "Номер порта зеленего цвета"
    desc: str = "Введите номер порта зеленего цвета на колонне"
    value: str = ""
    value_type: str = "string"


class OwenRedPort(EmbeddedModel):
    title: str = "Номер порта красного цвета"
    desc: str = "Введите номер порта красного цвета на колонне"
    value: str = ""
    value_type: str = "string"


class OwenYellowPort(EmbeddedModel):
    title: str = "Номер порта желтого цвета"
    desc: str = "Введите номер порта желтого цвета на колонне"
    value: str = ""
    value_type: str = "string"


class OwenBuzzerPort(EmbeddedModel):
    title: str = "Номер порта звукового сигнала"
    desc: str = "Введите номер порта звукового на колонне"
    value: str = ""
    value_type: str = "string"


class OwenPortsUsed(EmbeddedModel):
    title: str = "НЕ ИЗМЕНЯТЬ используемые порты OWEN"
    desc: str = "Используемые порты OWEN, не изменяйте это значение"
    value: str = ""
    value_type: str = "string"


class OwenSettings(EmbeddedModel):
    title: str = "Настройки OWEN"
    advanced: bool = True
    owen_ip: ERDIp = ERDIp(title="IP контроллера OWEN")
    owen_snmp_port: ERDSNMPPort = ERDSNMPPort(title="SNMP порт контроллера OWEN")
    owen_community_string: ERDCommunityString = ERDCommunityString()
    owen_oid: ERDFirstOID = ERDFirstOID(title="OID owen контроллера")
    owen_green_port: OwenGreenPort = OwenGreenPort()
    owen_yellow_port: OwenYellowPort = OwenYellowPort()
    owen_red_port: OwenRedPort = OwenRedPort()
    owen_buzzer_port: OwenBuzzerPort = OwenBuzzerPort()
    owen_ports_used: OwenPortsUsed = OwenPortsUsed()


class DropSignalDuration(EmbeddedModel):
    title: str = "Длительность сигнала при сбросе пачек"
    desc: str = "Введите длительность сигнала при сбросе пачек в секундах"
    value: int = 30
    value_type: str = "integer"


class AddQrToCubeSignalDuration(EmbeddedModel):
    title: str = "Длительность сигнала при сканировании QR куба"
    desc: str = "Введите длительность сигнала при сканировании QR в секундах"
    value: int = 3
    value_type: str = "integer"


class SignalSettings(EmbeddedModel):
    title: str = "Настройки сигналов на колонне"
    advanced: bool = False
    drop_signal_duration: DropSignalDuration = DropSignalDuration()
    add_qr_to_cube_signal_duration: AddQrToCubeSignalDuration = (
        AddQrToCubeSignalDuration()
    )
