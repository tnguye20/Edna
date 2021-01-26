export interface ApiResponse {
    data: Record<string, any>,
    status: number,
    statusText: string
}

export interface EdnaMeans {
    day: number,
    month: number,
    year: number
}

export interface EdnaBasicData {
    first_record_timestamp: string,
    last_record_timestamp: string,
    totalText: number,
    totalDay: number,
    totalMonth: number,
    years: number[],
    months: number[]
    means: EdnaMeans,
    participants: Array<string>,
    love_statistic: EdnaBasicData,
    miss_statistic: EdnaBasicData
}

export interface EdnaYearData extends EdnaBasicData {
    monthly_statistic: Record<string, EdnaBasicData>
}

export interface EdnaData extends EdnaBasicData {
    annual_statistic: Record<string, EdnaYearData>
}

export interface EdnaResponse extends ApiResponse {
    data: EdnaData
}

export interface ChartDataPoint {
    label: string,
    data: number
}

export type ChartDataPoints = ChartDataPoint[]

export interface FormattedData {
    annual_data: ChartDataPoints,
    monthly_data: ChartDataPoints
    masks_data: Record<string, Record<string, any>>
}

export type FormattedDataKey = keyof FormattedData;

export interface FormattedDataResponse extends ApiResponse {
    data: FormattedData
}