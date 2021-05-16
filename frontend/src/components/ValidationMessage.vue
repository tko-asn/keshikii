<template>
  <div v-show="messages.length">
    <p class="help" v-for="message in messages" :key="message">
      {{ message }}
    </p>
  </div>
</template>

<script>
export default {
  props: {
    messages: {
      type: Array,
      required: false,
    },
  },
};
</script>

<style scoped>
.help {
  color: red;
}
</style>