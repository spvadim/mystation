import { ProductionBatchParams } from "./ProductionBatchParams";

export interface Batch {
    number: {
        batch_number: number,
        batch_date: string
    },
    params: ProductionBatchParams,
    created_at?: string,
    closed_at?: string,
    id?: string
}

export interface BatchPut {
    number: {
        batch_number: number,
        batch_date: string,
    },
    params_id: string,
    id?: string,
}