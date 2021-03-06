from datetime import datetime
from typing import List, Optional

from odmantic.bson import ObjectId
from pydantic import BaseModel

from .model_config import ReportModelConfig
from .production_batch import ProductionBatchNumber


class PackReportItem(BaseModel):
    created_at: datetime
    qr: str
    barcode: str
    to_process: bool
    is_corrected: bool
    comments: List[str]

    Config = ReportModelConfig


class PackReportItemExtended(PackReportItem):
    id: ObjectId


class MPackReportItem(BaseModel):
    created_at: datetime
    qr: Optional[str]
    barcode: Optional[str]
    to_process: bool
    is_corrected: bool
    comments: List[str]
    packs: List[PackReportItem] = []

    Config = ReportModelConfig


class MPackReportItemExtended(MPackReportItem):
    packs: List[PackReportItemExtended] = []
    id: ObjectId


class CubeReportItem(BaseModel):
    created_at: datetime
    batch_number: ProductionBatchNumber
    qr: Optional[str]
    barcode: Optional[str]
    multipacks_in_cubes: int
    packs_in_multipacks: int
    to_process: bool
    is_corrected: bool
    comments: List[str]
    multipacks: List[MPackReportItem] = []

    Config = ReportModelConfig


class CubeReportItemExtended(CubeReportItem):
    multipacks: List[MPackReportItemExtended] = []
    id: ObjectId


class AnotherCubeReportItem(BaseModel):
    created_at: datetime
    batch_number: ProductionBatchNumber
    qr: Optional[str]
    barcode: Optional[str]
    multipacks_in_cubes: int
    packs_in_multipacks: int
    to_process: bool
    is_corrected: bool
    comments: List[str]
    packs: List[PackReportItem] = []

    Config = ReportModelConfig


class ReportRequest(BaseModel):
    report_begin: datetime
    report_end: datetime

    Config = ReportModelConfig


class ReportResponse(ReportRequest):
    cubes: List[CubeReportItem] = []


class ExtendedReportResponse(ReportRequest):
    cubes: List[CubeReportItemExtended] = []


class ReportWithoutMPacksResponse(ReportRequest):
    cubes: List[AnotherCubeReportItem] = []
