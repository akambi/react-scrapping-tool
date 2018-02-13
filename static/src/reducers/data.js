import { RECEIVE_PROTECTED_DATA, FETCH_PROTECTED_DATA_REQUEST,
    RECEIVE_PROTOCOL_META, REQUEST_PROTOCOL_META, OPEN_MENU, CLOSE_MENU, SELECT_SECTION } from '../constants';
import { createReducer } from '../utils/misc';

const initialState = {
    data: null,
    isFetching: false,
    loaded: false,
    openedMenu: false,
    selectedSection: null,
};

export default createReducer(initialState, {
    [RECEIVE_PROTECTED_DATA]: (state, payload) =>
        ({ ...state, ...{
            data: payload.data,
            isFetching: false,
            loaded: true,
        }}),
    [FETCH_PROTECTED_DATA_REQUEST]: (state) =>
        ({ ...state, ...{
            isFetching: true,
        }}),
    [RECEIVE_PROTOCOL_META]: (state, payload) =>
        ({ ...state, ...{ protocol_metas: {
            name: payload.name,
            data: payload.data,
            isFetching: false,
            loaded: true,
        }}}),
    [REQUEST_PROTOCOL_META]: (state) =>
        ({ ...state, ...{ protocol_metas: {
            isFetching: true,
        }}}),
    [OPEN_MENU]: (state) =>
        ({ ...state, ...{
            openedMenu: true,
        }}),
    [CLOSE_MENU]: (state) =>
        ({ ...state, ...{
            openedMenu: false,
        }}),
    [SELECT_SECTION]: (state, payload) => ({ ...state, ...{
            selectedSection: payload.section,
        }}),
});
