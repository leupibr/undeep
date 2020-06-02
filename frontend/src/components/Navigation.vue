<template>
  <nav class="navbar is-spaced is-fixed-top has-shadow"
       role="navigation" aria-label="main navigation">
    <div class="container">
      <div class="navbar-brand">
        <router-link to="/"
                     tag="a"
                     class="navbar-item">
          <i class="fas fa-file-invoice fa-2x"></i>
        </router-link>
      </div>

      <div class="navbar-menu">
        <div class="navbar-start">
          <div class="navbar-item has-dropdown is-hoverable">
            <router-link to="/" tag="a" class="navbar-link">Documents</router-link>
            <div class="navbar-dropdown">
              <router-link to="/recent?o=modified"
                           tag="a" class="navbar-item">
                <span class="icon has-text-grey"><i class="fas fa-user-edit"></i></span>
                <span>Recently Modified</span>
              </router-link>
              <router-link to="/recent?o=uploaded"
                           tag="a" class="navbar-item">
                <span class="icon has-text-grey"><i class="fas fa-user-clock"></i></span>
                <span>Recently Uploaded</span>
              </router-link>
            </div>
          </div>
        </div>
        <div class="navbar-end">
          <a class="navbar-item">
            <div class="field has-addons">
              <div class="control">
                <label>
                  <input class="input" type="text"
                         placeholder="Find a document"
                         v-model="term"
                         v-on:keyup.enter="search"
                         v-shortkey.focus="{a: ['ctrl', 'f'], b: ['shift', '/'], c: ['/']}"
                  >
                </label>
              </div>
              <div class="control">
                <a class="button is-info" v-on:click="search"><i class="fas fa-search"></i></a>
              </div>
            </div>
          </a>
          <div class="navbar-item has-dropdown is-hoverable" :class="{'is-active': scanning}">
            <a class="navbar-link">Actions</a>
            <div class="navbar-dropdown is-right">
              <a class="navbar-item"
                 v-on:click="this.scanDocument"
                 @shortkey="this.scanDocument"
                 v-shortkey.once="['alt', 'shift', 's']"
              >
                <span class="icon has-text-grey" v-if="scanning">
                  <i class="fas fa-spinner fa-pulse"></i></span>
                <span class="icon has-text-grey" v-if="!scanning">
                  <i class="fas fa-print"></i></span>
                <span>Scan Document</span>
              </a>
              <hr class="navbar-divider">
              <a class="navbar-item" v-on:click="this.recreateIndex">
                <span class="icon has-text-grey"><i class="fas fa-book-reader"></i></span>
                <span>Recreate Index</span>
              </a>
              <a class="navbar-item" v-on:click="this.learnCategories">
                <span class="icon has-text-grey"><i class="fas fa-user-graduate"></i></span>
                <span>Learn Categories</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Navigation',
  data() {
    return {
      term: '',
      scanning: false,
    };
  },
  methods: {
    search() {
      let q = encodeURI(this.term);
      if (q.trim() === '') {
        this.$eventBus.$emit('search-complete', [], null);
        return;
      }

      const route = this.$router.currentRoute;
      if (route.name !== 'Home') {
        this.$router.push({ name: 'Home' }, () => {
          if (route.params.category !== undefined && q.indexOf('category:') === -1) {
            q = `(${q}) AND category:${route.params.category}`;
            this.term = decodeURI(q);
          }

          axios.get(`documents/search?q=${q}`)
            .then((response) => {
              this.$eventBus.$emit('search-complete', response.data, this.term);
            });
        });
      } else {
        axios.get(`documents/search?q=${q}`)
          .then((response) => {
            this.$eventBus.$emit('search-complete', response.data, this.term);
          });
      }
    },
    scanDocument() {
      this.scanning = true;
      axios.post('documents/scan')
        .then((response) => {
          this.scanning = false;
          const scanned = response.data;
          if (scanned.length === 1) {
            this.$router.push({ name: 'ViewDocument', params: { id: scanned[0].path } });
          } else {
            this.$eventBus.$emit('store-changed');
          }
        })
        .catch(() => {
          this.scanning = false;
        });
    },
    recreateIndex() {
      axios.get('management/recreate-index')
        .then(() => { this.$eventBus.$emit('store-changed'); });
    },
    learnCategories() {
      axios.get('management/learn-categories')
        .then(() => { this.$eventBus.$emit('store-changed'); });
    },
  },
};
</script>
