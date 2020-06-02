<template>
  <tr>
    <td><i class="fas" v-bind:class="iconStyle"></i></td>
    <td>
      <router-link
        :to="{ name: 'ViewDocument', params: { id: value.path }}"
        tag="a">
        {{ value.name }}
      </router-link>
    </td>
    <td>{{ value.size|humanize }}</td>
    <td>{{ value.date|moment('ll') }}</td>
    <td>{{ value.modified|moment('ll') }}</td>
  </tr>
</template>

<script>
export default {
  name: 'DocumentElement',
  props: ['value'],
  computed: {
    iconStyle() {
      return {
        'fa-robot has-text-warning': this.value.method === 'Automatic',
        'fa-user-tag has-text-info': this.value.method === 'Manual',
        'fa-user-check has-text-success': this.value.method === 'Confirmed',
      };
    },
  },
};
</script>
