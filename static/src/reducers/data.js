import { RECEIVE_PROTECTED_DATA, FETCH_PROTECTED_DATA_REQUEST,
    RECEIVE_PROTOCOL_META, REQUEST_PROTOCOL_META } from '../constants';
import { createReducer } from '../utils/misc';

const initialState = {
    data: null,
    isFetching: false,
    loaded: false,
};

export default createReducer(initialState, {
    [RECEIVE_PROTECTED_DATA]: (state, payload) =>
        Object.assign({}, state, {
            data: payload.data,
            isFetching: false,
            loaded: true,
        }),
    [FETCH_PROTECTED_DATA_REQUEST]: (state) =>
        Object.assign({}, state, {
            isFetching: true,
        }),
    [RECEIVE_PROTOCOL_META]: (state, payload) =>
        Object.assign({}, state, { protocol_metas: {
            name: payload.name,
            data: payload.data,
            isFetching: false,
            loaded: true,
        }}),
    [REQUEST_PROTOCOL_META]: (state) =>
        Object.assign({}, state, { protocol_metas: {
            isFetching: true,
        }}),
});
