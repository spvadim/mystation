from typing import List

from fastapi import APIRouter, HTTPException, Query
from odmantic import ObjectId

from ..db.db_utils import (
    check_qr_unique,
    delete_multipack_by_id,
    get_batch_by_number_or_return_last,
    get_by_id_or_404,
    get_by_qr_or_404,
    get_last_batch,
    get_last_packing_table_amount,
    get_multipacks_queue,
    get_system_settings,
)
from ..db.engine import engine
from ..db.events import add_events
from ..models.multipack import (
    Multipack,
    MultipackEditSchema,
    MultipackOutput,
    MultipackPatchSchema,
)
from ..models.pack import Pack
from ..models.pack import Status as PackStatus
from ..utils.naive_current_datetime import get_naive_datetime
from .custom_routers import DeepLoggerRoute, LightLoggerRoute

deep_logger_router = APIRouter(route_class=DeepLoggerRoute)
light_logger_router = APIRouter(route_class=LightLoggerRoute)


@deep_logger_router.put("/multipacks", response_model=Multipack)
async def create_multipack(multipack: Multipack):
    batch = await get_batch_by_number_or_return_last(
        batch_number=multipack.batch_number
    )

    multipack.batch_number = batch.number
    multipack.created_at = await get_naive_datetime()

    packs_to_update = []
    for id in multipack.pack_ids:
        pack = await get_by_id_or_404(Pack, id)
        pack.in_queue = False
        packs_to_update.append(pack)
    await engine.save_all(packs_to_update)

    if multipack.qr:
        if not await check_qr_unique(Multipack, multipack.qr):
            raise HTTPException(
                400, detail=f"Мультипак с QR-кодом {multipack.qr} уже есть в системе"
            )
        multipack.added_qr_at = await get_naive_datetime()

    await engine.save(multipack)
    return multipack


@light_logger_router.get("/multipacks_queue", response_model=List[MultipackOutput])
async def get_current_multipacks():
    multipacks_queue = await get_multipacks_queue()
    return multipacks_queue


@light_logger_router.get("/multipacks/{id}", response_model=Multipack)
async def get_multipack_by_id(id: ObjectId):
    multipack = await get_by_id_or_404(Multipack, id)
    return multipack


@light_logger_router.get("/multipacks/", response_model=Multipack)
async def get_multipack_by_qr(qr: str = Query(None)):
    multipack = await get_by_qr_or_404(Multipack, qr)
    return multipack


@deep_logger_router.delete("/multipacks/{id}", response_model=Multipack)
async def remove_multipack_by_id(id: ObjectId):
    settings = await get_system_settings()
    if settings.general_settings.allow_delete_multipacks.value:
        return await delete_multipack_by_id(id)

    raise HTTPException(400, detail=f"Включена настройка, запрещающая удалять паллеты")


@deep_logger_router.delete(
    "/remove_multipacks_to_refresh_wrapper", response_model=List[Multipack]
)
async def remove_multipacks_to_refresh_wrapper():
    multipacks_amount = await get_last_packing_table_amount()
    current_batch = await get_last_batch()
    multipacks_to_delete_amount = current_batch.params.multipacks_after_pintset
    multipacks_to_delete = await get_multipacks_queue()
    multipacks_to_delete = multipacks_to_delete[
        multipacks_amount : multipacks_amount + multipacks_to_delete_amount
    ]

    if len(multipacks_to_delete) != multipacks_to_delete_amount:
        error_msg = "Недостаточно паллет для перезагрузки обмотчика"
        raise HTTPException(status_code=400, detail=error_msg)

    for multipack in multipacks_to_delete:
        await delete_multipack_by_id(multipack.id)

    return multipacks_to_delete


@deep_logger_router.patch("/multipacks/{id}", response_model=Multipack)
async def update_multipack_by_id(id: ObjectId, patch: MultipackPatchSchema):
    multipack = await get_by_id_or_404(Multipack, id)

    if patch.qr:
        if not await check_qr_unique(Multipack, patch.qr):
            raise HTTPException(
                400, detail=f"Мультипак с QR-кодом {patch.qr} уже есть в системе"
            )
        multipack.added_qr_at = await get_naive_datetime()

    patch_dict = patch.dict(exclude_unset=True)
    for name, value in patch_dict.items():
        setattr(multipack, name, value)
    await engine.save(multipack)
    return multipack


@deep_logger_router.patch("/edit_multipack/{id}", response_model=Multipack)
async def edit_multipack_by_id(id: ObjectId, edit_schema: MultipackEditSchema):
    multipack = await get_by_id_or_404(Multipack, id)
    batch_number = multipack.batch_number

    batch = await get_batch_by_number_or_return_last(batch_number=batch_number)
    max_packs_in_multipack = batch.params.packs

    pack_ids = multipack.pack_ids
    pack_qrs_to_add = edit_schema.pack_qrs
    pack_ids_to_delete = set(edit_schema.pack_ids_to_delete)
    packs_barcode = edit_schema.packs_barcode
    current_time = await get_naive_datetime()

    if (
        len(pack_ids) + len(pack_qrs_to_add) - len(pack_ids_to_delete)
        > max_packs_in_multipack
    ):
        raise HTTPException(
            400, f"Переполнение паллеты: пачек более чем {max_packs_in_multipack}"
        )

    removing_pack_ids = set(pack_ids).intersection(pack_ids_to_delete)
    remaining_pack_ids = pack_ids_to_delete - removing_pack_ids

    if remaining_pack_ids:
        raise HTTPException(
            404,
            f"В данной паллете не обнаружено пачек с такими id: {remaining_pack_ids}",
        )

    pack_ids = list(set(pack_ids) - removing_pack_ids)
    packs_to_delete = await engine.find(Pack, Pack.id.in_(list(removing_pack_ids)))

    packs_to_add = []
    for qr in pack_qrs_to_add:
        if not await check_qr_unique(Pack, qr):
            raise HTTPException(400, f"В системе уже существует пачка с QR={qr}")

        pack = Pack(
            qr=qr,
            barcode=packs_barcode,
            batch_number=batch_number,
            in_queue=False,
            created_at=current_time,
            status=PackStatus.ON_ASSEMBLY,
        )
        packs_to_add.append(pack)
        pack_ids.append(pack.id)

    multipack.pack_ids = pack_ids
    if edit_schema.is_corrected is not None:
        multipack.is_corrected = edit_schema.is_corrected
    if edit_schema.to_process is not None:
        multipack.to_process = edit_schema.to_process

    await engine.save_all(packs_to_add)
    for pack in packs_to_delete:
        await engine.delete(pack)

    alarm_tp_message = f"Camera=Back|Event=EditMultipack|DataQR={multipack.qr}|AdditionalInfo=MultipackId: {multipack.id}"
    await add_events("alarm_tp", alarm_tp_message)
    await engine.save(multipack)

    return multipack
