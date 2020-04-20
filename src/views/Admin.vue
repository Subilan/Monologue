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
          if (r.data === false) {
            this.$router.push({
              name: "admin-auth"
            })
          }
        }
      );
    }
  }
});
</script>

<style lang="less">
.admin {
  position: relative;
  height: 100%;
}

.admin-container {
  @media screen and (max-width: 1024px) {
    margin-left: 16px;
    margin-right: 16px;
  }
  margin-top: 56px;
  height: 100%;
  position: relative;
}

.hero {
  h1 {
    font-size: 48px;
  }

  p {
    color: #aaa;
    font-size: 24px;
  }
}
</style>