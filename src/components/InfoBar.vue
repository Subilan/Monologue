<template>
    <div class="information-bar">

    </div>
</template>

<script lang="ts">
import Vue from 'vue'
// @ts-ignore
import MdIcon from 'vue-material/dist/components/MdIcon';

Vue.use(MdIcon);

export default Vue.extend({
    
})
</script>

<style lang="less" scoped>
.information-bar {
	&.blue {
		background-color: @blue-light;
		color: @blue-primary;
	}

	&.red {
		background-color: @red-light;
		color: @red-primary;
	}

	&.green {
		background-color: @green-light;
		color: @green-primary;
	}
}
</style>