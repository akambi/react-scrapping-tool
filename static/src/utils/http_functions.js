/* eslint camelcase: 0 */

import axios from 'axios';

const tokenConfig = (token) => ({
    headers: {
        'Authorization': token, // eslint-disable-line quote-props
    },
});

export function validate_token(token) {
    return axios.post('/caps_api/is_token_valid', {
        token,
    });
}

export function get_github_access() {
    window.open(
        '/github-login',
        '_blank' // <- This is what makes it open in a new window.
    );
}

export function create_user(email, password) {
    return axios.post('/caps_api/create_user', {
        email,
        password,
    });
}

export function get_token(email, password) {
    return axios.post('/caps_api/get_token', {
        email,
        password,
    });
}

export function has_github_token(token) {
    return axios.get('/caps_api/has_github_token', tokenConfig(token));
}

export function data_about_user(token) {
    return axios.get('/caps_api/user', tokenConfig(token));
}

export function getProtocolMeta(protocolFile, token) {
    const url = '/caps_api/protocolscrapper';
    const formData = new FormData();
    formData.append('protocol_file', protocolFile)
    const config = {
        headers: {
            'content-type': 'multipart/form-data'
        }
    }
    return axios.post(url, formData, {...tokenConfig(token), ...config});
}


export function exportProtocolData(protocolData, token) {
    const url = '/caps_api/xmlgenerator';
    return axios.post(url, protocolData, {...tokenConfig(token)});
}
