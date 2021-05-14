<template>
  <div class="columns mt-6 is-marginless">
    <div class="column is-8 content">
      <p class="mb-5 title-p">自己紹介</p>
      <div>
        <p v-if="user.self_introduction">
          {{ user.self_introduction }}
        </p>
        <p v-else>自己紹介は未記入です。</p>
      </div>
    </div>
    <div class="column content">
      <p class="mb-5 title-p">アカウント作成日時</p>
      <div>
        <p>{{ user.registered_date }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["user"],
};
</script>

<style scoped>
.title-p {
  font-size: 1.2em;
}
</style>