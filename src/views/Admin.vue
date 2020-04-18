<template>
  <div class="admin">
    <router-view />
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
    mounted() {
        // this page is not for visiting, just for routing!
        if (this.$route.name === "admin") {
            this.$router.go(-1);
        }
    }
})
</script>

<style lang="less" scoped>
.admin {
    position: relative;
    height: 100%;
}
</style>