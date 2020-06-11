<template>
    <div id="app">
        <Navigation/>

        <main id="view">
            <router-view :key="$route.fullPath"/>
        </main>
        <Upload/>
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
