<template>
    <div class="functions">
        <slot></slot>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
    
})
</script>

<style lang="less" scoped>
.functions {
  @media screen and (max-width: 1024px) {
    display: none;
  }
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
</style>