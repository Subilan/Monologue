<template>
	<div v-if="auth" class="admin-panel admin-container">
		<div class="header">
			<div class="hero">
				<h1>控制中心</h1>
				<p>选择您要进行的操作</p>
			</div>
			<FunctionBar class="function-bar-float-right">
				<md-button @click="$router.push({ name: 'home' })" class="md-raised md-icon-button">
					<md-icon class="mdi mdi-home" />
				</md-button>
				<md-button @click="logoutConfirmDialog = true" class="md-raised md-icon-button">
					<md-icon class="mdi mdi-logout" />
				</md-button>
				<md-button class="md-raised md-icon-button">
					<md-icon class="mdi mdi-help-circle" />
				</md-button>
			</FunctionBar>
		</div>
		<div class="function-group">
			<div @click="goto('admin-new-event')" class="function">
				<h1>添加新事件</h1>
				<p>添加新的事件以展示在首页的时间线内，可以是公告、已解决或者问题。</p>
				<span class="icon mdi mdi-alert-decagram" />
			</div>
			<div @click="goto('admin-new-vote')" class="function">
				<h1>创建投票</h1>
				<p>创建投票以快速收集用户观点数据，将数据归档或用作进一步处理。</p>
				<span class="icon mdi mdi-chart-bar" />
			</div>
			<div class="function">
				<h1>创建反馈区</h1>
				<p>创建一个反馈区收集留言，将留言用作实际计划的参考和改进依据。</p>
				<span class="icon mdi mdi-forum" />
			</div>
			<div class="function">
				<h1>设置</h1>
				<p>编辑用户信息，配置和管理 Monologue 本体的行为和数据处理方式。</p>
				<span class="icon mdi mdi-cogs" />
			</div>
			<div class="function">
				<h1>关于 Monologue</h1>
				<p>查看 Monologue 的版本信息、更新日志和更多相关的技术层面内容。</p>
				<span class="icon mdi mdi-information-variant" />
			</div>
		</div>
		<md-dialog :md-active.sync="logoutConfirmDialog">
			<md-dialog-title>{{ logoutCompleted ? "登出成功" : logoutFailed ? "登出失败" : logoutConfirmed ? "正在登出..." : "登出确认" }}</md-dialog-title>
			<md-dialog-content>
				{{ logoutCompleted ? "您已成功登出，即将跳转至首页。" : logoutFailed ? "由于内部问题，此时无法登出。" : logoutConfirmed ? "" : "是否确实要登出？您可以稍后重新登录。" }}
				<div class="text-align-center" v-if="logoutConfirmed && !logoutFailed && !logoutCompleted">
					<md-progress-spinner style="display: inline-flex" md-mode="indeterminate" />
				</div>
			</md-dialog-content>
			<md-dialog-actions>
				<md-button v-if="!logoutConfirmed" class="md-primary" @click="logoutConfirmDialog = false">取消</md-button>
				<md-button v-if="!logoutConfirmed" class="md-primary md-raised" @click="logout()">确定</md-button>
				<md-button v-if="logoutConfirmed && (logoutFailed || logoutCompleted)" class="md-primary" @click="logoutConfirmDialog = false">好</md-button>
			</md-dialog-actions>
		</md-dialog>
		<md-snackbar md-position="center" :md-duration="1500" :md-active.sync="snackbar">{{ snackbarMessage }}</md-snackbar>
	</div>
</template>

<script lang="ts">
import Vue from "vue";
import FunctionBar from "@/components/FunctionBar.vue";

export default Vue.extend({
	data() {
		return {
			auth: false,
			snackbar: false,
			snackbarMessage: "",
			logoutConfirmDialog: false,
			logoutConfirmed: false,
			logoutCompleted: false,
			logoutFailed: false,
		};
	},
	components: {
		FunctionBar
	},
	created() {
		this.$server.post(
			"/api/auth",
			{
				method: "auth"
			},
			r => {
				if (!r.data) {
					this.$router.push({
						name: "admin-auth"
					});
				} else {
					this.auth = true;
				}
			}
		);
	},
	methods: {
		logout() {
			this.logoutConfirmed = true;
			this.$server.post(
				"/api/auth",
				{
					method: "logout"
				},
				r => {
					if (r.data) {
						this.logoutCompleted = true;
						setTimeout(() => {
							this.$router.push({
								name: "home"
							})
						}, 1500);
					} else {
						this.logoutFailed = true;
					}
				}
			);
		},
		goto(name: string) {
			this.$router.push({
				name
			});
		}
	}
});
</script>

<style lang="less" scoped>
.function-group {
	@media screen and (min-width: 1024px) {
		display: flex;
		margin-top: 8px;
		margin-bottom: 8px;
		flex-wrap: wrap;

		&:first-child {
			margin-top: 0;
		}
		&:last-child {
			margin-bottom: 0;
		}
	}
	display: grid;

	.function {
		@media screen and (min-width: 1024px) {
			margin-left: 8px;
			margin-right: 8px;
			&:nth-child(3n + 1) {
				margin-left: 0;
			}

			&:nth-child(3n + 3) {
				margin-right: 0;
			}

			&:nth-child(n + 4) {
				margin-top: 16px;
			}
			width: calc(33.3% - 43px);
		}

		@media screen and (max-width: 1024px) {
			margin-top: 8px;
			margin-bottom: 8px;
			&:nth-child(3n + 1) {
				margin-top: 16px;
			}
			&:nth-child(3n + 3) {
				margin-bottom: 0;
			}
		}
		background-color: #eee;
		padding: 16px;
		border-radius: 2px;
		position: relative;
		opacity: 1;
		transition: linear opacity 0.2s;
		cursor: pointer;
		line-height: 1.8;
		box-sizing: content-box;

		h1 {
			line-height: 1;
		}

		&:focus,
		&:hover {
			opacity: 0.6;
			transition: linear opacity 0.2s;
		}

		.icon {
			color: rgba(0, 0, 0, 0.21);
			position: absolute;
			&::before {
				font-size: 72px;
			}
			bottom: 0;
			right: 16px;
			z-index: 1;
		}
	}
}

.header {
	display: flex;
	align-items: center;
	width: 100%;
}
</style>
