<template>
	<div class="admin-editor">
		<router-view />

		<md-dialog :md-active.sync="routerConfirmDialog">
			<md-dialog-title>跳转确认</md-dialog-title>
			<md-dialog-content>是否确认要跳转到其它页面？未保存的更改将永久消失。</md-dialog-content>
			<md-dialog-actions>
				<md-button
					@click="
						next();
						routerConfirmDialog = false;
					"
					class="md-primary"
					>跳转</md-button
				>
				<md-button @click="routerConfirmDialog = false" class="md-primary md-raised">取消</md-button>
			</md-dialog-actions>
		</md-dialog>
	</div>
</template>

<script lang="ts">
import Vue from "vue";
// @ts-ignore
import MdDialog from "vue-material/dist/components/MdDialog";

Vue.use(MdDialog);

export default Vue.extend({
	data() {
		return {
			routerConfirmDialog: false,
			ignoreConfirm: false,
		};
	},
	methods: {
		next() {}
	},
	beforeRouteLeave(to, from, next) {
		if (this.$store.state.editorCommited || this.ignoreConfirm) {
			next();
		} else {
			this.next = next;
			this.routerConfirmDialog = true;
			next(false);
		}
	},
	mounted() {
		if (this.$route.matched.length === 1) {
			this.ignoreConfirm = true;
			this.$router.push({
				name: "admin-panel"
			})
		}
	}
});
</script>

<style lang="less" scoped>
.admin-editor {
	height: 100%;
	position: relative;
}
</style>
