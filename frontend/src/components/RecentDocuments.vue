<template>
  <div class="panel" v-if="documents.length > 0">
    <p class="panel-heading">Recent Documents</p>

    <div class="panel-block" v-if="documents.length > 0">
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
  </div>
</template>

<script>
import axios from 'axios';
import DocumentElement from '@/components/DocumentElement';

export default {
  name: 'RecentDocuments',
  components: { DocumentElement },
  data() {
    return {
      documents: [],
    };
  },
  methods: {
    updateRecentDocuments() {
      axios.get('documents/recent')
        .then((response) => {
          this.documents = response.data.documents;
        });
    },
  },
  beforeMount() {
    this.updateRecentDocuments();
  },
  mounted() {
    this.$eventBus.$on('store-changed', this.updateRecentDocuments);
  },
};
</script>
