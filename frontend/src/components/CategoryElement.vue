<template>
  <div class="column has-text-centered is-one-fifth">
    <router-link
      :to="{ name: 'ViewCategory', params: { category: value.name }}"
      tag="a"
      class="box has-text-info category">
      <div class="tag is-danger is-rounded">{{value.count}}</div>
      <i class="fas fa-folder fa-5x symbol">
        <i class="fas fa-robot has-text-grey-lighter predictions"
           v-if="value.predictions > 0"></i>
      </i>
      <span class="heading">{{value.name}}</span>
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'CategoryElement',
  props: ['value'],
};
</script>
