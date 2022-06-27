from odmantic import EmbeddedModel


class PintsetIp(EmbeddedModel):
    title: str = "Ip контроллера пинцета"
    desc: str = "Введите IP контроллера пинцета"
    value: str
    value_type: str = "string"


class PintsetRack(EmbeddedModel):
    title: str = "Rack контроллера пинцета"
    desc: str = "Введите Rack контроллера пинцета"
    value: int
    value_type: str = "integer"


class PintsetSlot(EmbeddedModel):
    title: str = "Slot контроллера пинцета"
    desc: str = "Введите Slot контоллера пинцета, нужно вводить слот основного CPU"
    value: int
    value_type: str = "integer"


class PintsetTCPPort(EmbeddedModel):
    title: str = "TCP port контроллера пинцета"
    desc: str = "Введите TCP port контоллера пинцета"
    value: int = 102
    value_type: str = "integer"


class PintsetDbName(EmbeddedModel):
    title: str = "Область памяти контроллера пинцета"
    desc: str = "Введите номер области памяти контроллера пинцета"
    value: int
    value_type: str = "integer"


class PintsetStartingByte(EmbeddedModel):
    title: str = "Начальный байт контроллера пинцета"
    desc: str = "Введите начальный байт контроллера пинцета"
    value: int
    value_type: str = "integer"


class PintsetReadingLength(EmbeddedModel):
    title: str = "Сколько байтов считывает контроллер пинцета"
    desc: str = "Введите количество считываемых байтов контроллером пинцета"
    value: int
    value_type: str = "integer"


class PintsetByteNumber(EmbeddedModel):
    title: str = "Номер изменяемого байта контроллера пинцета"
    desc: str = "Введите номер изменяемого байта контроллера пинцета"
    value: int
    value_type: str = "integer"


class PintsetBitNumber(EmbeddedModel):
    title: str = "Номер изменяемого бита"
    desc: str = "Введите номер изменяемого бита контроллера пинцета"
    value: int
    value_type: str = "integer"


class PintsetStartingByte(EmbeddedModel):
    title: str = "Начальный байт контроллера пинцета"
    desc: str = "Введите начальный байт контроллера пинцета"
    value: int
    value_type: str = "integer"


class EjectorStartingByte(EmbeddedModel):
    title: str = "Начальный байт контроллера пинцета для предварительного сброса"
    desc: str = "Введите начальный байт контроллера пинцета"
    value: int = 12
    value_type: str = "integer"


class EjectorReadingLength(EmbeddedModel):
    title: str = (
        "Сколько байтов считывает контроллер пинцета для предварительного сброса"
    )
    desc: str = "Введите количество считываемых байтов контроллером пинцета"
    value: int = 1
    value_type: str = "integer"


class EjectorByteNumber(EmbeddedModel):
    title: str = (
        "Номер изменяемого байта контроллера пинцета для предварительного сброса"
    )
    desc: str = "Введите номер изменяемого байта контроллера пинцета"
    value: int = 0
    value_type: str = "integer"


class EjectorBitNumber(EmbeddedModel):
    title: str = "Номер изменяемого бита для предварительного сброса"
    desc: str = "Введите номер изменяемого бита контроллера пинцета"
    value: int = 2
    value_type: str = "integer"


class EjectorDropValue(EmbeddedModel):
    title: str = "Значение, при котором контроллер осуществляет предварительный сброс"
    desc: str = (
        "Выберите значение, при котором контроллер осуществляет предварительный сброс"
    )
    value: bool = True
    value_type: str = "bool"


class PintsetTurningOffValue(EmbeddedModel):
    title: str = "Значение, при котором контроллер останавливает пинцет"
    desc: str = "Выберите значение, при котором контроллер останавливает пинцет"
    value: bool
    value_type: str = "bool"


class PintsetTurningOnValue(EmbeddedModel):
    title: str = "Значение, при котором контроллер включает пинцет"
    desc: str = "Выберите значение, при котором контроллер включает пинцет"
    value: bool
    value_type: str = "bool"


class PintsetCurtainOpeningDuration(EmbeddedModel):
    title: str = "На сколько секунд замораживается пинцет (0 -- саморазмораживание)"
    desc: str = (
        "Введите, на сколько секунд замораживается пинцет, при ненулевых значениях"
        " после истечения времени отдается команда на разморозку (Учалы), при нулевом"
        " значении команда на разморозку НЕ отдается (Юрга)"
    )
    value: int = 10
    value_type: str = "integer"


class PintsetDelayBeforeFreezing(EmbeddedModel):
    title: str = "Задержка перед заморозкой пинцета"
    desc: str = "Введите задержку в секундах"
    value: float = 0
    value_type: str = "float"


class PintsetSettings(EmbeddedModel):
    title: str = "Настройки пинцета"
    advanced: bool = True
    pintset_ip: PintsetIp
    pintset_rack: PintsetRack
    pintset_slot: PintsetSlot
    pintset_tcp_port: PintsetTCPPort = PintsetTCPPort()
    pintset_db_name: PintsetDbName
    pintset_starting_byte: PintsetStartingByte
    pintset_reading_length: PintsetReadingLength
    pintset_byte_number: PintsetByteNumber
    pintset_bit_number: PintsetBitNumber
    ejector_starting_byte: EjectorStartingByte = EjectorStartingByte()
    ejector_reading_length: EjectorReadingLength = EjectorReadingLength()
    ejector_byte_number: EjectorByteNumber = EjectorByteNumber()
    ejector_bit_number: EjectorBitNumber = EjectorBitNumber()
    ejector_drop_value: EjectorDropValue = EjectorDropValue()
    pintset_turning_off_value: PintsetTurningOffValue
    pintset_turning_on_value: PintsetTurningOnValue
    pintset_curtain_opening_duration: PintsetCurtainOpeningDuration = (
        PintsetCurtainOpeningDuration()
    )
    pintset_delay_before_freezing: PintsetDelayBeforeFreezing = (
        PintsetDelayBeforeFreezing()
    )
