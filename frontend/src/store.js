import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';
import createPersistedState from 'vuex-persistedstate';

Vue.use(Vuex);

const getDefaultState = () => ({ token: '', user: {} });

export default new Vuex.Store({
    strict: true,
    plugins: [createPersistedState()],
    state: getDefaultState(),
    getters: {
        isLoggedIn: (state) => state.token !== '',
        getUser: (state) => state.user,
    },
    mutations: {
        SET_TOKEN: (state, token) => {
            state.token = token;
        },
        SET_USER: (state, user) => {
            state.user = user;
        },
        RESET: (state) => {
            Object.assign(state, getDefaultState());
        },
    },
    actions: {
        login: ({ commit }, { token, user }) => {
            commit('SET_TOKEN', token);
            commit('SET_USER', user);
            axios.defaults.headers.common.Authorization = `Token ${token}`;
        },
        logout: ({ commit }) => {
            commit('RESET', '');
            delete axios.defaults.headers.common.Authorization;
        },
    },
});
