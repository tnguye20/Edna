import * as React from 'react';
import { useAuthValue } from '../../contexts';
import { edna } from '../../api';
import { ChartDataPoint, ChartDataPoints, FormattedData, FormattedDataKey } from '../../Interfaces';

import {
  Grid,
  Container,
  Typography
} from '@material-ui/core';
import { 
    LineChart, 
    Line, 
    CartesianGrid,
    XAxis, 
    YAxis,
    Tooltip,
    ResponsiveContainer
} from 'recharts';
import { nodeModuleNameResolver } from 'typescript';

const CHART_TITLES = {
    annual_data: 'Annual Texts Summary',
    monthly_data: 'Monthly Texts Summary',
    masks_data: 'Custom Phrases Summary'
};

type ChartTitle = keyof FormattedData;

export const Main: React.FunctionComponent = () => {
    const { authUser } = useAuthValue();
    const [formattedData, setFormattedData] = React.useState({} as FormattedData);

    React.useEffect(() => {
        const get = async () => {
            try {
                const { data } = await edna.getFormattedData(authUser.idToken);
                setFormattedData(data);
            }
            catch(error) {
                console.log(error);
            }
        }
        get();
    }, [authUser.idToken]);

    return (
        <Container>
            <Grid
                container
                spacing={0}
                direction="column"
                justify="center"
                style={{ minHeight: '100vh'}}
            >
                <Typography
                    align="center"
                    variant="h4"
                    gutterBottom
                >
                    The Edna
                </Typography>
                {
                    Object.keys(formattedData).length > 0
                    ? (
                        Object.entries(formattedData)
                        .filter((entry) => entry[0] !== 'masks_data')
                        .map((entry) => {
                            const [key, data] = entry;
                            return (
                                <Grid item xs={12} sm={12}>
                                    <BasicLineChart data={data} title={CHART_TITLES[key as ChartTitle]}/>
                                </Grid>
                            );
                        })
                    )
                    : ''
                }
                {
                    Object.keys(formattedData).length > 0
                    ? (
                        Object.keys(formattedData.masks_data)
                        .map((mask) => {
                            const data = Object.keys(formattedData.masks_data[mask])
                            .reduce((accumulator, current: string) => {
                                if(isNaN(parseFloat(current))){
                                    return accumulator;
                                }
                                return [...accumulator, formattedData.masks_data[mask][current]]
                            }, [] as ChartDataPoints);

                            return (
                                <Grid item xs={12} sm={12}>
                                    <BasicLineChart data={data} title={mask}/>
                                </Grid>
                            );
                        })
                    ) : ''
                }
            </Grid>
        </Container>
    )
}

const BasicLineChart = (props: React.PropsWithoutRef<any>) => {
    const { data, title } = props;
    return (
        <>
            <Typography
                align="center"
                variant="h6"
                gutterBottom
            >
                {title ? title : 'Chart'}
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                    <Line type="monotone" dataKey="data" stroke="#8884d8" />
                    <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                    <XAxis dataKey="label" />
                    <YAxis />
                    <Tooltip />
                </LineChart>
            </ResponsiveContainer>
        </>
    )
}