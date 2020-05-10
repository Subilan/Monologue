<template>
	<div class="admin-event admin-container">
		<Editor :editingTitle="editingTitle" :editingContent="editingContent" :loading="loading" @submit="submit($event)">
			<template #hero>
				<h1>{{ editing ? "编辑事件 #" + id : "添加新事件" }}</h1>
				<p>{{ editing ? "修改该事件的内容和相关属性。" : "在时间线上添加新的事件以供外部参考。" }}</p>
			</template>
			<template #toolbar>
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
			<md-dialog-content>是否要确认删除此事件？此操作无法回滚。</md-dialog-content>
			<md-dialog-actions>
				<md-button
					@click="
						deleteEvent();
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
				<md-field>
					<md-icon class="mdi" :class="getIconByType()" />
					<label>选择事件类型</label>
					<md-select required v-model="type">
						<md-option value="info">一般</md-option>
						<md-option value="warning">警告</md-option>
						<md-option value="solved">已解决</md-option>
					</md-select>
				</md-field>
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

export default Vue.extend({
	data() {
		return {
			editingTitle: "",
			editingContent: "",
			type: "info",
			id: -1,
			titleInvalid: "",
			contentInvalid: "",
			snackbar: false,
			snackbarMessage: "",
			disableSubmit: false,
			invalidID: false,
			deleteConfirmDialog: false,
			configurationDialog: false,
			actioned: false,
			loading: false,
			editing: false
		};
	},
	components: {
		Editor
	},
	methods: {
		getIconByType() {
			let match: StringMatch = {
				info: "mdi-information-outline",
				warning: "mdi-alert-outline",
				solved: "mdi-check"
			};
			return match[this.type];
		},
		isEditing() {
			return this.$route.name === "admin-edit-event";
		},
		validate(title: string, content: string, type: string) {
			return title.length > 0 && title.length < 30 && content.length > 0 && content.length < 1000 && ["info", "warning", "solved"].includes(type);
		},
		submit(data: EditorResult) {
			if (this.disableSubmit) {
				return false;
			}
			// Do not let the empty data in, or the frontend array building process will blow up.
			if (!this.validate(data.title, data.content, this.type)) {
				this.snackbarMessage = "发送失败，请检查您填写的内容。";
				this.snackbar = true;
				return false;
			}
			this.$server.post(
				"/api/logue",
				{
					method: this.editing ? "alter" : "submit",
					title: data.title,
					contents: data.content,
					type: this.type,
					id: this.id
				},
				r => {
					if (r.data) {
						this.disableSubmit = true;
						this.snackbarMessage = "成功发布新的事件，即将为您跳转";
						this.$store.commit(this.$mutations.CHANGE_EDITOR_COMMITED_STATE, {
							state: true
						});
						this.snackbar = true;
						this.actioned = true;
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
		deleteEvent() {
			this.$server.post(
				"/api/logue",
				{
					method: "delete",
					id: this.id
				},
				r => {
					if (r.data) {
						this.snackbarMessage = "成功删除此事件，即将返回首页";
						this.snackbar = true;
						this.actioned = true;
						setTimeout(() => {
							this.$router.push({
								name: "home"
							});
						}, 1500);
					} else {
						this.snackbarMessage = "删除失败，请检查控制台";
						this.snackbar = true;
					}
				}
			);
		},
		next() {}
	},
	mounted() {
		this.editing = this.isEditing();
		if (this.editing) {
			this.loading = true;
			this.id = Number(this.$route.params.id);
			if (this.id > 0 && Number.isInteger(this.id) && this.id !== NaN) {
				this.$server.get("/api/logue?method=id&markdown=false&id=" + this.id, r => {
					let data = r.data;
					if (r.data) {
						this.editingTitle = data.title;
						this.editingContent = data.contents;
						this.type = data.type;
					} else {
						this.$store.commit(this.$mutations.CHANGE_EDITOR_COMMITED_STATE, {
							state: true
						});
						this.$router.push({
							name: "error-not-found"
						});
					}
					this.loading = false;
				});
			} else {
				this.$store.commit(this.$mutations.CHANGE_EDITOR_COMMITED_STATE, {
					state: true
				});
				this.$router.push({
					name: "error-not-found"
				});
			}
		}
		this.$store.commit(this.$mutations.CHANGE_EDITOR_COMMITED_STATE, {
			state: false
		});
	}
});
</script>

<style lang="less">
.admin-container {
	height: 100%;
	position: relative;
}
</style>
