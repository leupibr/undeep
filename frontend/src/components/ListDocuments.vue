<template>
    <div class="container">
        <div class="content">
            <label v-if="isCategory">
                <input class="title input is-fullwidth"
                       type="text"
                       v-if="isCategory"
                       v-model="category"
                       @change="changeName()"
                />
            </label>
            <h1 v-else class="title">{{getTitle}}</h1>
        </div>

        <div class="content" v-if="isCategory">
            <div class="buttons is-right">
                <a class="button is-danger" v-on:click="showConfirmation = true">
                    <span class="icon"><i class="fas fa-trash"></i></span>
                    <span>Delete Category</span>
                </a>
            </div>
        </div>

        <div class="panel" v-if="documents !== null">
            <table class="table is-hoverable is-striped is-narrow is-fullwidth">
                <thead>
                <tr>
                    <th></th>
                    <th>Name</th>
                    <th>Size</th>
                    <th>Date</th>
                    <th>Modified</th>
                </tr>
                </thead>
                <tbody>
                <DocumentElement v-for="d in documents" v-bind:value="d" v-bind:key="d.path"/>
                </tbody>
            </table>
        </div>

        <Paginate
            :total="this.total"
            :limit="this.limit"
            :current="this.offset"
            v-on:goto="this.goto"
            v-if="limit < total"/>

        <DeleteConfirmation
            :title="`Delete ${this.category}?`"
            @confirm="deleteCategory"
            @abort="showConfirmation = false"
            v-if="showConfirmation">
            <p>Do you really want to delete this category <b>irreversible</b>?</p>
            <p class="mt-4" v-if="total > 0">
                All documents will loose the category assignment and need to be reclassified manually.
                It's strongly recommended to learn the categories again after the documents are cleaned up.
            </p>
        </DeleteConfirmation>
    </div>
</template>

<script>
    import axios from 'axios';
    import DocumentElement from '@/components/DocumentElement';
    import Paginate from '@/components/Paginate';
    import DeleteConfirmation from './DeleteConfirmation';

    export default {
        name: 'ListDocuments',
        components: { DeleteConfirmation, Paginate, DocumentElement },
        data() {
            return {
                order: null,
                category: null,

                offset: 0,
                limit: 15,
                total: null,
                documents: null,

                showConfirmation: false,
            };
        },
        computed: {
            isCategory() {
                return this.category != null;
            },
            getTitle() {
                if (this.category) return this.category;
                if (this.order === 'modified') return 'Recently Modified';
                if (this.order === 'uploaded') return 'Recently Uploaded';
                return 'Recent Documents';
            },
        },
        methods: {
            getUrl(offset = null) {
                const getOffset = offset != null ? offset : this.offset;
                if (this.$route.params.category) {
                    return `categories/${this.$route.params.category}/documents/${getOffset}/${this.limit}`;
                }
                return `documents/recent/${this.$route.query.o}/${getOffset}/${this.limit}`;
            },
            loadDocuments() {
                axios.get(this.getUrl())
                    .then((response) => {
                        const d = response.data;
                        this.total = parseInt(d.total, 10);
                        this.documents = d.documents;
                    });
            },
            goto(offset) {
                axios.get(this.getUrl(offset))
                    .then((response) => {
                        const d = response.data;
                        this.offset = offset;
                        this.total = parseInt(d.total, 10);
                        this.documents = d.documents;
                    });
            },
            changeName() {
                axios.put(`categories/${this.$route.params.category}`, { name: this.category })
                    .then(() => {
                        this.$router.replace({
                            name: 'ViewCategory',
                            params: { category: this.category },
                            query: this.$route.query,
                        });
                    })
                    .catch((error) => {
                        this.$notify({
                            title: 'Unable to rename category',
                            text: `(${error.response.status}) ${error.response.data.message}`,
                            type: 'is-danger',
                        });
                    });
            },
            deleteCategory() {
                this.showConfirmation = false;
                axios.delete(`categories/${this.category}`)
                    .then(() => {
                        this.$router.replace({ name: 'Home' });
                    });
            },
        },
        beforeRouteUpdate(to, from, next) {
            // skip intercept if it's a renaming
            if (from.params.category !== to.params.category) {
                next();
                return;
            }

            this.order = to.query.o;
            this.category = to.params.category;
            this.loadDocuments();
            next();
        },
        beforeMount() {
            this.order = this.$route.query.o;
            this.category = this.$route.params.category;
            this.loadDocuments();
        },
    };
</script>
