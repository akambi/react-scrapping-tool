import { RECEIVE_PROTECTED_DATA, FETCH_PROTECTED_DATA_REQUEST,
    RECEIVE_PROTOCOL_META, REQUEST_PROTOCOL_META, OPEN_MENU, CLOSE_MENU,
    SELECT_SECTION, REQUEST_EXPORT_XML, RECEIVE_EXPORT_XML } from '../constants';
import { createReducer } from '../utils/misc';

const initialState = {
    data: null,
    isFetching: false,
    loaded: false,
    openedMenu: false,
    selectedSection: null,
    selectedSubSection: null,
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
    [RECEIVE_PROTOCOL_META]: (state, payload) => {
        if (!payload.data) {
            return { ...state }
        }

        const sections = [...new Set(payload.data.protocoldata.map(item => item.section))]
        payload.data.protocoldata = payload.data.protocoldata
                                        .map(item => ({ ...item, subSection: item.id.split('.', 2).join('.')
                                        .toUpperCase() }));

        const subSections = [...new Set(payload.data.protocoldata.map(item => item.subSection))];
        let subSectionsByGrp = [];
        subSections.forEach((item) => {
            const section = item.split('.', 2)[0];
            if (!subSectionsByGrp[section]) {
                subSectionsByGrp[section] = [];
            }
            subSectionsByGrp[section].push(item.toUpperCase());
        });

        return ({ ...state, ...{ protocol_metas: {
            name: payload.name,
            data: payload.data,
            isFetching: false,
            loaded: true,
        }, sections, subSections: subSectionsByGrp, selectedSection: sections.length && sections[0] }});
    },
    [REQUEST_PROTOCOL_META]: (state, payload) =>
        ({ ...state, ...{ protocol_metas: {
            name: payload.name,
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
            selectedSubSection: payload.subSection,
        }}),
    [REQUEST_EXPORT_XML]: (state, payload) =>
        ({ ...state, ...{ isFetchingExport: true }}),
    [RECEIVE_EXPORT_XML]: (state, payload) => ({ ...state, ...{ isFetchingExport: false } }),
});
