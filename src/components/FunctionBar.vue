<template>
	<div>
		<div v-if="pc || singleOnMobile" class="functions">
			<div class="items">
				<slot></slot>
			</div>
		</div>

		<md-menu :class="is('home') ? 'home-scoped' : ''" v-if="!pc && !singleOnMobile" md-direction="bottom-start" class="mobile-menu-btn">
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
import { isPCView } from "@/functions";

Vue.use(MdMenu)
	.use(MdList)
	.use(MdIcon)
	.use(MdButton);

export default Vue.extend({
	props: ["auth"],
	data() {
		return {
			singleOnMobile: false,
			pc: false
		};
	},
	methods: {
		isPCView,
		is(name: string) {
			return this.$route.name === name;
		}
	},
	mounted() {
		// @ts-ignore
		if (((this.$slots.default.length === 2 && this.$slots.default[0].tag === undefined) || this.$slots.default.length === 1) && (!this.is("home") || !this.auth)) {
			this.singleOnMobile = true;
		}
		this.pc = isPCView();
	}
});
</script>

<style lang="less" scoped>
.mobile-menu-btn {
	position: absolute;
	top: -16px;
	right: 0;

	&.home-scoped {
		top: 16px !important;
	}
}

.mobile-menu {
	display: flex;
	align-items: center;
}

.functions {
	.fontfamily-default;

	@media screen and (max-width: 1024px) {
		top: -16px;
	}

	@media screen and (min-width: 1024px) {
		top: 32px;
	}

	position: absolute;
	right: 0;
	display: flex;
	flex-direction: row;
	align-items: center;
	width: 100%;

	> * {
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
