import * as React from 'react';
import { useAuthValue } from '../../contexts';
import { edna } from '../../api';
import { ChartDataPoints, FormattedData } from '../../Interfaces';

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

export const Main: React.FunctionComponent = () => {
    const { authUser } = useAuthValue();
    const [chartAnnualData, setChatAnnualData] = React.useState([] as ChartDataPoints);
    const [chartMonthlyData, setChatMonthlyData] = React.useState([] as ChartDataPoints);

    React.useEffect(() => {
        const get = async () => {
            try {
                const { data } = await edna.getFormattedData(authUser.idToken);
                setChatAnnualData(data.annual_data);
                setChatMonthlyData(data.monthly_data);
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
                <Grid item xs={12} sm={12}>
                    <Typography
                        align="center"
                        variant="h6"
                        gutterBottom
                    >
                        Annual Text
                    </Typography>
                    <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={chartAnnualData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                            <Line type="monotone" dataKey="data" stroke="#8884d8" />
                            <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                            <XAxis dataKey="label" />
                            <YAxis />
                            <Tooltip />
                        </LineChart>
                    </ResponsiveContainer>
                </Grid>

                <Grid item xs={12} sm={12}>
                    <Typography
                        align="center"
                        variant="h6"
                        gutterBottom
                    >
                        Monthly Text
                    </Typography>
                    <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={chartMonthlyData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                            <Line type="monotone" dataKey="data" stroke="#8884d8" />
                            <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                            <XAxis dataKey="label" />
                            <YAxis />
                            <Tooltip />
                        </LineChart>
                    </ResponsiveContainer>
                </Grid>
            </Grid>
        </Container>
    )
}