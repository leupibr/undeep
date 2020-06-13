// src/services/AuthService.js
import axios from 'axios';

export default {
    login(credentials) {
        return axios
            .post('login', credentials)
            .then((response) => response.data);
    },
    logout() {
        return axios
            .post('logout')
            .then((response) => response.data);
    },
};
