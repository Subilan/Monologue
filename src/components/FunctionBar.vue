<template>
  <div>
    <div v-if="isPC()" class="functions">
      <slot></slot>
    </div>

    <md-menu v-if="!isPC()" md-direction="bottom-start" class="mobile-menu-btn">
      <md-button md-menu-trigger class="md-raised md-icon-button">
        <md-icon class="mdi mdi-plus-circle" />
      </md-button>
      <md-menu-content class="mobile-menu">
        <slot></slot>
      </md-menu-content>
    </md-menu>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
// @ts-ignore
import MdMenu from "vue-material/dist/components/MdMenu";
// @ts-ignore
import MdList from "vue-material/dist/components/MdList";
// @ts-ignore
import MdIcon from "vue-material/dist/components/MdIcon";
// @ts-ignore
import MdButton from "vue-material/dist/components/MdButton";
import { isPC } from "@/functions";

Vue.use(MdMenu)
  .use(MdList)
  .use(MdIcon)
  .use(MdButton);

export default Vue.extend({
  methods: {
    isPC
  }
});
</script>

<style lang="less" scoped>
.functions {
  position: absolute;
  top: 32px;
  right: 0;
  display: flex;
  align-items: center;

  * {
    margin-left: 8px;
    margin-right: 8px;

    &:first-child {
      margin-left: 0;
    }

    &:last-child {
      margin-right: 0;
    }
  }
}

.mobile-menu-btn {
  position: absolute;
  top: -16px;
  right: 0;
}

.mobile-menu {
  display: flex;
  align-items: center;
}
</style>