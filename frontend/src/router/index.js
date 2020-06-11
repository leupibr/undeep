import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/components/Home';
import ViewDocument from '@/components/ViewDocument';
import ListDocuments from '@/components/ListDocuments';

Vue.use(Router);

export default new Router({
    routes: [
        { path: '/', name: 'Home', component: Home },
        { path: '/view/:id', name: 'ViewDocument', component: ViewDocument },
        { path: '/category/:category', name: 'ViewCategory', component: ListDocuments },
        {
            path: '/recent/', name: 'Recent', query: { o: 'uploaded' }, component: ListDocuments,
        },
    ],
});
