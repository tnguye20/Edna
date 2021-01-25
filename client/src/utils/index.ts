import { 
    EdnaYearData,
    EdnaBasicData,
    EdnaData,
    ChartDataPoints
} from '../Interfaces';

export const processAnnualData = (data: EdnaData): ChartDataPoints => {
    const annual_statistic = Object.values(data.annual_statistic).map((yearly_data: EdnaYearData) => {
        const { years, totalText } = yearly_data;
        return {
            label: years.toString(),
            data: totalText,
        }
    });

    return annual_statistic;
};

export const processMonthlyData = (data: EdnaData) => {
    const dataPoints: ChartDataPoints = [];
    data.years.forEach((y: number) => {
        const year = y.toString();
        const months = data.annual_statistic[year].months;
        console.log(months);

        months.forEach((month: number) => {
            const monthly_data = data.annual_statistic[year].monthly_statistic[month.toString()];
            dataPoints.push({
                label: `${year}-${month}`,
                data: monthly_data.totalText
            });
        })
    });

    return dataPoints;
};