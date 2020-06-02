<template>
  <div class="panel" v-if="term !== null">
    <p class="panel-heading">
      Search Result
      <a class="delete is-pulled-right" v-on:click="onSearchComplete(null, null)" ></a>
    </p>

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

    <div class="panel-block has-text-centered" v-if="documents.length <= 0">
      <article class="media">
        <figure class="media-left">
          <p class="image">
            <i class="far fa-sad-tear fa-5x"></i>
          </p>
        </figure>
        <div class="media-content">
          <div class="content">
            Your search - <strong>{{term | truncate(5)}}</strong> - did not match any documents.
            <ul class="is-narrow">
              <li>Make sure that all words are spelled correctly.</li>
              <li>Try different keywords.</li>
              <li>Try more general keywords.</li>
              <li>Try fewer keywords.</li>
            </ul>
          </div>
        </div>
      </article>
    </div>
  </div>
</template>

<script>
import DocumentElement from '@/components/DocumentElement';

export default {
  name: 'SearchResult',
  components: { DocumentElement },
  data() {
    return {
      term: null,
      documents: null,
    };
  },
  methods: {
    onSearchComplete(result, term) {
      this.term = term;
      this.documents = result;
    },
  },
  mounted() {
    this.$eventBus.$on('search-complete', this.onSearchComplete);
  },
};
</script>
