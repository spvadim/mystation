export interface ProductionBatchInput {
    number:	{
        batch_number: number,
        batch_date: string
    },
    params_id: string,
    id?: string
}