<template>
  <div class="panel">
    <div class="columns is-multiline">
      <counter-element v-model="documents">Documents</counter-element>
      <counter-element v-model="categories">Categories</counter-element>
      <counter-element v-model="labels">Labels</counter-element>
      <counter-element v-model="storage" :size="true">Storage</counter-element>
      <counter-element v-model="index" :size="true">Index</counter-element>
      <counter-element v-model="model" :size="true">Model</counter-element>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Vue from 'vue';

Vue.component('counter-element', {
  props: ['value', 'size'],
  template: `
    <div class="column is-one-fifth has-text-centered" v-if="value !== null">
      <div>
        <p class="heading"><slot></slot></p>
        <p class="title" v-if="size">{{value|humanize(false, 2)}}</p>
        <p class="title" v-if="!size">{{value}}</p>
      </div>
    </div>
  `,
});

export default {
  name: 'Counter',
  data() {
    return {
      documents: null,
      categories: null,
      labels: null,
      storage: null,
      index: null,
      model: null,
    };
  },
  methods: {
    updateDocumentCount() {
      axios.get('documents/count')
        .then((response) => {
          this.documents = response.data;
        });
    },
    updateCategoryCount() {
      axios.get('categories/count')
        .then((response) => {
          this.categories = response.data;
        });
    },
    updateStatistics() {
      axios.get('statistics/storage')
        .then((response) => {
          this.storage = response.data.documents;
          this.index = response.data.index;
          this.model = response.data.model;
        });
    },
  },
  beforeMount() {
    this.updateDocumentCount();
    this.updateCategoryCount();
    this.updateStatistics();
  },
  mounted() {
    this.$eventBus.$on('store-changed', this.updateDocumentCount);
    this.$eventBus.$on('store-changed', this.updateStatistics);
  },
};
</script>
