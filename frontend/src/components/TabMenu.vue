<template>
  <div class="tabs is-centered">
    <ul>
      <li
        :class="{ 'is-active': index === isActive }"
        @click="switchIsActive(index)"
        v-for="(tab, index) in tabNameList"
        :key="tab"
      >
        <a>
          {{ tab }}
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: ["routesList", "tabNameList", "option"],
  data() {
    return {
      active: 0,
    };
  },
  methods: {
    switchIsActive(tabIndex) {
      if (this.routesList.length) {
        // タブをクリックしてページ遷移が行われる場合
        const newRouteName = this.routesList[tabIndex];
        if (this.$route.name !== newRouteName) {
          this.$router.replace({ name: newRouteName });
        }
      } else {
        // タブをクリックしてもページ遷移を行わず表示内容を条件分岐で切り替える場合
        this.$emit("returnTabIndex", tabIndex);
        this.active = tabIndex;
      }
    },
  },
  computed: {
    isActive() {
      // タブをクリックしてページ遷移が行われる場合
      if (this.routesList.length) {
        return this.routesList.indexOf(this.$route.name);
      } else {
        // タブをクリックしてもページ遷移を行わず表示内容を条件分岐で切り替える場合
        return this.active;
      }
    },
  },
  watch: {
    option() {
      // ページ遷移しないタブ移動で親からもタブを移動させたいときpropsのoptionからactiveの値を変換。
      if (this.option) {
        this.active = this.option;
        this.$emit("resetOption");
      }
    },
  },
};
</script>