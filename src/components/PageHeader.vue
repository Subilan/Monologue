<template>
	<div class="header">
		<div class="hero">
			<slot />
		</div>
		<function-bar class="function-bar-float-right">
			<slot name="functions" />
			<slot name="default-functions" />
		</function-bar>
	</div>
</template>

<script lang="ts">
import Vue from "vue";
import FunctionBar from "@/components/FunctionBar.vue";

export default Vue.extend({
	components: {
		FunctionBar
	}
});
</script>
