<template>
    <div class="admin">
        <div class="loading" v-if="$route.name === 'admin'">
            <md-progress-spinner md-mode="indeterminate" />
        </div>
        <transition :name="fade" mode="out-in">
            <router-view />
        </transition>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
// @ts-ignore
import MdProgress from "vue-material/dist/components/MdProgress";

Vue.use(MdProgress);

export default Vue.extend({
    data() {
        return {
            fade: ""
        };
    },
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
                        });
                    } else {
                        this.$router.push({
                            name: "admin-panel"
                        });
                    }
                }
            );
        }
    },
    watch: {
        $route(to, from) {
            // TODO: 针对不同方向跳转设置过渡
            this.fade = "fade";
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

.fade-enter,
.fade-leave-to {
    visibility: hidden;
    opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.2s ease;
}

.fade-enter-to,
.fade-leave {
    opacity: 1;
    visibility: visible;
}
</style>