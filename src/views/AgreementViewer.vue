<template>
	<div class="agreement-viewer full-height">
		<div class="header">
			<h1>{{ title }}</h1>
		</div>
		<div class="contents typo" v-html="content" />
	</div>
</template>

<script lang="ts">
import Vue from "vue";
// @ts-ignore
import MdCheckbox from "vue-material/dist/components/MdIcon";
// @ts-ignore
import MdEmptyState from "vue-material/dist/components/MdEmptyState";

Vue.use(MdCheckbox)
	.use(MdEmptyState);

export default Vue.extend({
	data() {
		return {
			id: "",
			title: "",
			content: "",
			disagreement: false
		};
	},
	created() {
		this.id = this.$route.params.id;
		this.$server.get("/api/agreement?markdown=true&id=" + this.id, r => {
			if (r.data) {
				let data = r.data;
				this.title = data.title;
				this.content = data.contents;
				this.disagreement = data.disagreement;
			} else {
				this.$router.push({
					name: "error-not-found"
				});
			}
		});
	}
});
</script>

<style lang="less" scoped>
.header {
	h1 {
		text-align: center;
		font-size: 64px;
		line-height: 1.8;
	}
}

.contents {
	margin-top: 32px;
	margin-bottom: 32px;
	.typo {
		p {
			font-size: 28px !important;
		}
	}

	&::selection {
		.selection;
	}
}
</style>
