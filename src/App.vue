<template>
    <div class="app container">
        <info-bar @click.native="$router.go(0)" color="red" class="layout-alert" :class="pc ? 'pc' : 'mobile'">
			<md-icon class="mdi mdi-alert" />
			需要刷新以显示正常布局
		</info-bar>
        <transition name="fade" mode="out-in">
            <router-view />
        </transition>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import InfoBar from "@/components/InfoBar.vue";
import { isPCView } from '@/functions';

export default Vue.extend({
    data() {
        return {
            pc: false,
        }
    },
    components: {
        InfoBar,
    },
    mounted() {
        this.pc = isPCView();
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

.layout-alert {
	&.pc {
		@media screen and (min-width: 1024px) {
			display: none;
		}
	}

	&.mobile {
		@media screen and (max-width: 1024px) {
			display: none;
		}
	}
}
</style>