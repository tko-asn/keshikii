<template>
  <div>
    <router-view></router-view>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  mounted() {
    window.addEventListener("click", this.closeDropDown);
  },
  computed: {
    ...mapGetters("dropdown", ["isOpen", "isDown"]),
  },
  methods: {
    closeDropDown(e) {
      if (
        !e.target.closest("#dropdown-menu") &&
        !e.target.closest("#dropdown-trigger")
      ) {
        if (this.isDown) {
          this.$store.dispatch("dropdown/changeIsDown", false);
        }
      }
      if (
        !e.target.closest("#burger-menu") &&
        !e.target.closest("#burger-button")
      ) {
        if (this.isOpen) {
          this.$store.dispatch("dropdown/changeIsOpen", false);
        }
      }
    },
  },
};
</script>