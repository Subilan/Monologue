<template>
    <div class="app container">
        <transition name="fade" mode="out-in">
            <router-view />
        </transition>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
    mounted() {}
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