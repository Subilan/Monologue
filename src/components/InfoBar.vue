<template>
	<div class="information-bar" :class="[color]" :style="{opacity}" v-if="!disabled">
		<slot></slot>
	</div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
	props: ["color"],
	data() {
		return {
			opacity: 1,
			disabled: false,
		}
	},
	mounted() {
		let lastScrollTop = 0;
		let st;
		window.onscroll = e => {
			st = window.pageYOffset || document.documentElement.scrollTop;
			if (st > lastScrollTop) {
				this.opacity = 0;
			} else {
				this.opacity = 1;
			}
			lastScrollTop = st <= 0 ? 0 : st;
		}
	}
});
</script>

<style lang="less" scoped>
.information-bar {
	&.blue {
		&,
		.mdi::before {
			background-color: @blue-light;
			color: @blue-primary;
		}
	}

	&.red {
		&,
		.mdi::before {
			background-color: @red-light;
			color: @red-primary;
		}
	}

	&.green {
		&,
		.mdi::before {
			background-color: @green-light;
			color: @green-primary;
		}
	}

	.mdi {
		&:first-child {
			margin-right: 16px;
		}

		&:last-child {
			margin-left: 16px;
		}
	}

	.fontfamily-default;
	z-index: 1000;
	font-weight: 500;
	width: 100%;
	display: flex;
	align-items: center;
	justify-content: center;
	position: fixed;
	font-size: 18px;
	top: 0;
	left: 0;
	height: 48px;
	transition: opacity .2s ease;
	cursor: pointer;
}
</style>
