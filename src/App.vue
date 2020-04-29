<template>
    <div class="app container">
        <transition name="fade" mode="out-in">
            <router-view />
        </transition>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import { getcookie, setcookie } from "@/cookie";
import bus from '@/bus';

export default Vue.extend({
    mounted() {
        if (getcookie("ft") === undefined) {
            setcookie("ft", true);
        } else if (getcookie("ft") === true) {
            bus.$emit("first-time-event", null);
        }
        bus.$on("first-time-event-cancle", p => {
            setcookie("ft", false);
        })
    }
});
</script>

<style lang="less" scoped>
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