from enum import Enum
from typing import Optional

from odmantic import EmbeddedModel, Model, ObjectId

from .model_config import ModelConfig


class WorkMode(str, Enum):
    AUTO = "auto"
    MANUAL = "manual"
    SEMIAUTO = "semi-auto"


class State(str, Enum):
    NORMAL = "normal"
    WARNING = "warning"
    ERROR = "error"


class SyncState(str, Enum):
    NORMAL = "normal"
    ERROR = "error"
    FIXING = "fixing"


class Mode(EmbeddedModel):
    work_mode: WorkMode = WorkMode.AUTO


class SystemState(EmbeddedModel):
    state: State = State.NORMAL
    pintset_state: State = State.NORMAL
    pintset_withdrawal_state: State = State.NORMAL
    packing_table_state: State = State.NORMAL
    sync_state: SyncState = SyncState.NORMAL
    error_msg: Optional[str]
    pintset_error_msg: Optional[str]
    packing_table_error_msg: Optional[str]
    pintset_withdrawal_error_msg: Optional[str]
    sync_error_msg: Optional[str]
    wrong_cube_id: Optional[ObjectId]
    next_pack_is_second: bool = False


class SystemStatus(Model):
    mode: Mode
    system_state: SystemState
    multipack_coded_by_qr: bool = False

    Config = ModelConfig
