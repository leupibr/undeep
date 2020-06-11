<template>
  <div class="container">
    <h1 class="title">{{getTitle}}</h1>

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
      v-if="limit < total"
    />
  </div>
</template>

<script>
import axios from 'axios';
import DocumentElement from '@/components/DocumentElement';
import Paginate from '@/components/Paginate';

export default {
  name: 'ListDocuments',
  components: { Paginate, DocumentElement },
  data() {
    return {
      order: null,
      category: null,

      offset: 0,
      limit: 15,
      total: null,
      documents: null,
    };
  },
  computed: {
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
  },
  beforeRouteUpdate(to, from, next) {
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
