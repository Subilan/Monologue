<template>
  <div class="admin">
    <router-view />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  mounted() {
    // this page is not for visiting, just for routing!
    if (this.$route.name === "admin") {
      this.$server.post(
        "/api/auth",
        {
          method: "auth"
        },
        r => {
          if (r.data) {
            this.$router.push({
              name: "admin-panel"
            });
          } else {
            this.$router.push({
              name: "admin-auth"
            });
          }
        }
      );
    }
  }
});
</script>

<style lang="less" scoped>
.admin {
  position: relative;
  height: 100%;
}
</style>