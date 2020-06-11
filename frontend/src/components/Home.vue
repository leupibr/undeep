<template>
    <div class="container">
        <Counter/>
        <SearchResult/>
        <Categories/>
        <RecentDocuments/>
    </div>
</template>

<script>
    import Counter from '@/components/Counter';
    import SearchResult from '@/components/SearchResult';
    import RecentDocuments from '@/components/RecentDocuments';
    import Categories from '@/components/Categories';

    export default {
        name: 'Home',
        components: { Categories, RecentDocuments, Counter, SearchResult },
    };
</script>
