import { FETCH_PROTECTED_DATA_REQUEST, RECEIVE_PROTECTED_DATA,
 REQUEST_PROTOCOL_META, RECEIVE_PROTOCOL_META, OPEN_MENU, CLOSE_MENU,
 SELECT_SECTION, REQUEST_EXPORT_XML, RECEIVE_EXPORT_XML, CHANGE_FIELD_VALUE } from '../constants/index';
import { parseJSON } from '../utils/misc';
import { data_about_user, getProtocolMeta, exportProtocolData } from '../utils/http_functions';
import { logoutAndRedirect } from './auth';
import { browserHistory } from 'react-router';

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

export function requestProtocolMeta(protocolFile) {
    return {
        type: REQUEST_PROTOCOL_META,
        payload: {
            name: protocolFile.name,
        },
    };
}

export function processProtocol(protocolFile, token) {
    return (dispatch) => {
        dispatch(requestProtocolMeta(protocolFile));
        browserHistory.push('/result');
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

export function receiveExportXML(protocolFile, data) {
    return {
        type: RECEIVE_EXPORT_XML,
        payload: {
            name: protocolFile,
            data,
        },
    };
}

export function requestExportXML() {
    return {
        type: REQUEST_EXPORT_XML,
    };
}

export function exportProtocolToXML(protocolFile, protocolData, token) {
    return (dispatch) => {
        dispatch(requestExportXML());
        exportProtocolData(protocolData, token)
            .then(response => {
                dispatch(receiveExportXML(protocolFile, response.data));
            })
            .catch(error => {
                dispatch(receiveExportXML({}));
                if (error.status === 403) {
                    dispatch(logoutAndRedirect(error));
                }
            });
    };
}

export function openMenu() {
    return {
        type: OPEN_MENU,
    };
}

export function closeMenu() {
    return {
        type: CLOSE_MENU,
    };
}

export function selectSection(section, subSection) {
    return {
        type: SELECT_SECTION,
        payload: {
            section,
            subSection,
        },
    };
}

export function changeFieldValue(field, value) {
    return {
        type: CHANGE_FIELD_VALUE,
        payload: {
            field,
            value
        }
    };
}
