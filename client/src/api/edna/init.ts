import axios from 'axios';
import { ROUTES } from '../../constants';

export const init = async (uid: string, filename: string) => {
    try {
        const url = ROUTES.API_EDNA_INIT;
        const options = {
            headers: {
                "AUTH-TOKEN": uid
            }
        };
        const _data = {
            filename
        };

        const { status, statusText, data } = await axios.post(url, _data, options);
        return {
        status, statusText, data
        };
    }
    catch (error) {
        if (error.response) {
            const { status } = error.response;
            const { errorMsg, errorTitle, message } = error.response.data;
            throw new Error(message ? message : errorMsg);
        }
        throw new Error('Unexpected Error Happened. Please try again in a few minutes.');
    }
}