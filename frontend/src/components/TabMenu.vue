<template>
  <div class="tabs is-centered">
    <ul>
      <!-- タブ -->
      <li
        :class="{ 'is-active': index === isActive }"
        @click="switchIsActive(index)"
        v-for="(tab, index) in tabNameList"
        :key="tab"
      >
        <!-- タブ名 -->
        <a>
          {{ tab }}
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    routesList: {
      type: Array,
      default: () => [],
    },
    tabNameList: {
      type: Array,
      default: () => [],
    },
    option: {
      default: false,
    },
  },
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
        // タブをクリックしてもページ遷移を行わず表示内容を
        // 条件分岐で切り替える場合
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
        // タブをクリックしてもページ遷移を行わず表示内容を
        // 条件分岐で切り替える場合
        return this.active;
      }
    },
  },
  watch: {
    option() {
      // ページ遷移しないタブ移動で親からもタブを移動させたいとき
      // propsのoptionからactiveの値を変換
      if (this.option || this.option === 0) {
        this.active = this.option;
        this.$emit("resetOption");
      }
    },
  },
};
</script>