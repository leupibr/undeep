<template>
    <div class="panel" v-if="categories !== null">
        <div class="columns is-multiline">
            <CategoryElement
                v-for="c in categories"
                v-bind:key="c.name"
                v-bind:value="c"/>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import CategoryElement from '@/components/CategoryElement';

    export default {
        name: 'Categories',
        components: { CategoryElement },
        data() {
            return { categories: null };
        },
        methods: {
            loadCategories() {
                axios.get('categories')
                    .then((response) => {
                        this.categories = response.data;
                    });
            },
        },
        beforeMount() {
            this.loadCategories();
        },
    };
</script>

<style>
    .category {
        position: relative;
    }

    .category .tag {
        position: absolute;
        top: 1rem;
        right: 1rem;
    }

    .category .symbol {
        position: relative;
    }

    .category .predictions {
        position: absolute;
        font-size: 1rem;
        bottom: 1rem;
        right: .5rem;
    }
</style>
