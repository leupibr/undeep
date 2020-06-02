import Vue from 'vue';
import axios from 'axios';
import moment from 'moment';
import 'bulma/css/bulma.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import '@fortawesome/fontawesome-free';

import App from './App';
import router from './router';

Vue.config.productionTip = false;

axios.defaults.baseURL = 'api/';
// axios.defaults.baseURL = 'http://localhost:8000/api/';
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';

Vue.prototype.$eventBus = new Vue();

Vue.use(require('vue-shortkey'));

Vue.filter('truncate', (text, length, suffix = '…') => {
    if (text.length <= length) return text;
    return text.substring(0, length) + suffix;
});

Vue.filter('humanize', (value, binary = false, precision = 0) => {
    // Converts number of bytes into a human readable format.
    // Function adopted from from https://stackoverflow.com/a/54131913/5494186
    if (value === 0) return '0 B';
    const base = binary ? 1024 : 1000;
    const multiple = Math.floor(Math.log2(value) / Math.log2(base));
    const converted = value / (base ** multiple);
    const s = binary ? 'i' : '';
    const m = ['B', `k${s}B`, `M${s}B`, `G${s}B`, `T${s}B`, `P${s}B`, `E${s}B`, `Z${s}B`, `Y${s}B`];

    return converted.toFixed(precision).concat(' ', m[multiple]);
});

Vue.filter('moment', (text, format) => moment(text).format(format));

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    components: { App },
    template: '<App/>',
});
