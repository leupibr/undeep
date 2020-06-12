<template>
    <div id="app">
        <Navigation/>

        <main id="view">
            <router-view :key="$route.fullPath" />
        </main>

        <notifications>
            <template slot="body" slot-scope="props">
                <div :class="`notification mt-3 mr-3 ${props.item.type}`">
                    <button class="delete" @click="props.close"></button>
                    <p class="has-text-weight-bold" v-if="props.item.title">{{props.item.title}}</p>
                    <p v-html="props.item.text"></p>
                </div>
            </template>
        </notifications>

        <Upload v-if="this.$store.getters.isLoggedIn"/>
    </div>
</template>

<script>
    import Navigation from '@/components/Navigation';
    import Upload from '@/components/Upload';

    export default {
        name: 'App',
        components: {
            Upload,
            Navigation,
        },
    };
</script>

<style>
    #app {
        padding-top: 5.25rem;
    }

    #view {
        padding: 3rem;
    }

    .panel {
        box-shadow: none;
    }
</style>
