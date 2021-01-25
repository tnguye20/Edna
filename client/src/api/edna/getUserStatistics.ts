import axios from 'axios';
import { ROUTES } from '../../constants';
import { EdnaResponse } from '../../Interfaces';

export const getUserStatistics = async (token: string): Promise<EdnaResponse> => {
    try {
        const url = ROUTES.API_EDNA_GET_STATISTICS;
        const options = {
            headers: {
                "AUTH-TOKEN": token
            }
        };

        const { status, statusText, data } = await axios.get(url, {
            ...options 
        });
        return {
            status, statusText, data
        };
    }
    catch (error) {
        if (error.response) {
            // const { status } = error.response;
            const { errorMsg, message } = error.response.data;
            throw new Error(message ? message : errorMsg);
        }
        throw new Error('Unexpected Error Happened. Please try again in a few minutes.');
    }
}