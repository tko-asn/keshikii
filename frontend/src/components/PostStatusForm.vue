<template>
  <div class="field mt-5 vertical-align">
    <div class="control">
      <label class="radio">
        <input
          type="radio"
          value="public"
          v-model="status"
          @change="clickRadioButton"
        />
        公開
      </label>
      <label class="radio">
        <input
          type="radio"
          value="private"
          v-model="status"
          @change="clickRadioButton"
        />
        非公開
      </label>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    origin: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      status: "public",
      count: 0,
    };
  },
  methods: {
    clickRadioButton() {
      this.$emit("changeRadio", this.status);
    },
  },
  watch: {
    // originに値が与えられていて、
    // statusへの代入が一回目なら代入を実行
    origin(val) {
      if (val) {
        if (!this.count) {
          this.status = val;
          this.count += 1;
        }
      }
    },
  },
};
</script>

<style scoped>
.vertical-align input {
  vertical-align: middle;
}
</style>