<template>
	<div class="admin-agreement">
		<Editor :editingTitle="editingTitle" :editingContent="editingContent" :loading="loading" :invalid="invalidID" @submit="submit($event)">
			<template v-slot:hero>
				<h1>{{ isEdit() ? "编辑协议 #" + id : "创建协议" }}</h1>
				<p>{{ isEdit() ? "修改协议的内容。" : "创建协议并收集同意或不同意协议的人员。" }}</p>
			</template>
			<template v-slot:toolbar>
				<md-button v-if="editing" @click="deleteConfirmDialog = true" class="md-icon-button md-raised">
					<md-icon class="mdi mdi-delete" />
				</md-button>
				<md-button @click="$router.push({ name: 'admin-panel' })" class="md-icon-button md-raised">
					<md-icon class="mdi mdi-cogs" />
				</md-button>
				<md-button @click="configurationDialog = true" class="md-icon-button md-raised">
					<md-icon class="mdi mdi-card-bulleted" />
				</md-button>
			</template>
		</Editor>
		<md-snackbar :md-active.sync="snackbar" md-position="center" :md-duration="1500" md-persistent>{{ snackbarMessage }}</md-snackbar>
		<md-dialog :md-active.sync="deleteConfirmDialog">
			<md-dialog-title>删除确认</md-dialog-title>
			<md-dialog-content>是否要确认删除此协议？此操作无法回滚。</md-dialog-content>
			<md-dialog-actions>
				<md-button
					@click="
						deleteAgreement();
						deleteConfirmDialog = false;
					"
					class="md-primary"
					>确认删除</md-button
				>
				<md-button @click="deleteConfirmDialog = false" class="md-primary md-raised">取消</md-button>
			</md-dialog-actions>
		</md-dialog>
		<md-dialog :md-active.sync="configurationDialog">
			<md-dialog-title>配置</md-dialog-title>
			<md-dialog-content>
				<md-checkbox v-model="allowDisagreement" class="md-primary">允许反对意见</md-checkbox>
			</md-dialog-content>
			<md-dialog-actions>
				<md-button class="md-primary md-raised" @click="configurationDialog = false">OK</md-button>
			</md-dialog-actions>
		</md-dialog>
	</div>
</template>

<script lang="ts">
import Vue from "vue";
import Editor from "@/components/Editor.vue";
import { stringToBoolean } from "@/functions";

export default Vue.extend({
	data() {
		return {
			id: -1,
			invalidID: false,
			loading: false,
			allowDisagreement: false,
			editing: false,
			editingTitle: "",
			editingContent: "",
			deleteConfirmDialog: false,
			configurationDialog: false,
			snackbar: false,
			snackbarMessage: "",
			disableSubmit: false
		};
	},
	methods: {
		isEdit() {
			return this.$route.name === "admin-edit-agreement";
		},
		validate(title: string, content: string, allowdisagreement: boolean) {
			return title.length > 0 && title.length <= 30 && content.length > 0 && content.length <= 1000 && typeof allowdisagreement === "boolean";
		},
		submit(e: EditorResult) {
			if (this.disableSubmit) {
				return false;
			}
			if (!this.validate(e.title, e.content, this.allowDisagreement)) {
				this.snackbarMessage = "发送失败，请检查您填写的内容。";
				this.snackbar = true;
				return false;
			}
			this.$server.post(
				"/api/agreement",
				{
					method: this.editing ? "alter" : "submit",
					title: e.title,
					contents: e.content,
					disagreement: this.allowDisagreement,
					id: this.editing ? this.id : -1
				},
				r => {
					if (r.data) {
						this.$store.commit(this.$mutations.CHANGE_EDITOR_COMMITED_STATE, {
							state: true
						});
						this.disableSubmit = true;
						this.snackbarMessage = "成功发布新的协议，即将为您跳转";
						this.snackbar = true;
						setTimeout(() => {
							this.$router.push({
								name: "admin-panel"
							});
						}, 1500);
					} else {
						this.snackbarMessage = "发送失败，请检查控制台";
						this.snackbar = true;
					}
				}
			);
		},
		deleteAgreement() {
			this.$server.post(
				"/api/agreement",
				{
					method: "delete",
					id: this.id
				},
				r => {
					if (r.data) {
						this.$store.commit(this.$mutations.CHANGE_EDITOR_COMMITED_STATE, {
							state: true
						});
						this.snackbarMessage = "成功删除此协议，即将返回首页";
						this.snackbar = true;
						setTimeout(() => {
							this.$router.push({
								name: "admin-panel"
							});
						}, 1500);
					} else {
						this.snackbarMessage = "删除失败，请检查控制台";
					}
				}
			);
		}
	},
	components: {
		Editor
	},
	created() {
		this.editing = this.isEdit();
		if (this.editing) {
			this.loading = true;
			this.$server.get("/api/agreement?id=" + this.$route.params.id, r => {
				this.loading = false;
				if (r.data) {
					let data = r.data;
					this.editingTitle = data.title;
					this.editingContent = data.contents;
					this.allowDisagreement = stringToBoolean(data.disagreement);
				} else {
					this.$store.commit(this.$mutations.CHANGE_EDITOR_COMMITED_STATE, {
						state: true
					});
					this.$router.push({
						name: "error-not-found"
					});
				}
			});
		}
		this.id = Number(this.$route.params.id);
		this.$store.commit(this.$mutations.CHANGE_EDITOR_COMMITED_STATE, {
			state: false
		});
	}
});
</script>

<style lang="less" scoped>
.admin-agreement {
	height: 100%;
	position: relative;
	padding: 16px;
	padding-bottom: 0;
	.agreement-content {
		height: 70% !important;
		position: relative;
		.agreement-content-input {
			height: 100% !important;
			position: relative;
		}
	}
}
</style>
