from typing import Optional

from odmantic.bson import ObjectId
from pydantic import BaseModel

from .model_config import ModelConfig


class IdModel(BaseModel):
    pack_id: ObjectId
    multipack_id: Optional[ObjectId] = None
    cube_id: Optional[ObjectId] = None

    Config = ModelConfig
