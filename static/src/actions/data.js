import { FETCH_PROTECTED_DATA_REQUEST, RECEIVE_PROTECTED_DATA,
 REQUEST_PROTOCOL_META, RECEIVE_PROTOCOL_META  } from '../constants/index';
import { parseJSON } from '../utils/misc';
import { data_about_user, getProtocolMeta } from '../utils/http_functions';
import { logoutAndRedirect } from './auth';

export function receiveProtectedData(data) {
    return {
        type: RECEIVE_PROTECTED_DATA,
        payload: {
            data,
        },
    };
}

export function fetchProtectedDataRequest() {
    return {
        type: FETCH_PROTECTED_DATA_REQUEST,
    };
}

export function fetchProtectedData(token) {
    return (dispatch) => {
        dispatch(fetchProtectedDataRequest());
        data_about_user(token)
            .then(parseJSON)
            .then(response => {
                dispatch(receiveProtectedData(response.result));
            })
            .catch(error => {
                if (error.status === 401) {
                    dispatch(logoutAndRedirect(error));
                }
            });
    };
}

export function receiveProtocolMeta(protocolFile, data) {
    return {
        type: RECEIVE_PROTOCOL_META,
        payload: {
            name: protocolFile.name,
            data,
        },
    };
}

export function requestProtocolMeta() {
    return {
        type: REQUEST_PROTOCOL_META,
    };
}

export function processProtocol(protocolFile, token) {
    return (dispatch) => {
        dispatch(requestProtocolMeta());
        getProtocolMeta(protocolFile, token)
            .then(parseJSON)
            .then(response => {
                dispatch(receiveProtocolMeta(protocolFile, response));
            })
            .catch(error => {
                if (error.status === 403) {
                    dispatch(logoutAndRedirect(error));
                }
            });
    };
}