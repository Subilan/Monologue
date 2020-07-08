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
		<h1>功能</h1>
		<div class="function-group">
			<div @click="goto('admin-new-event')" class="function" active>
				<h1>添加新事件</h1>
				<p>添加新的事件以展示在首页的时间线内，可以是公告、已解决或者问题。</p>
				<span class="icon mdi mdi-alert-decagram" />
			</div>
			<div @click="goto('admin-new-vote')" class="function" active>
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
				<h1>创建问卷</h1>
				<p>设计不同类型的不同题目，以流程化的方式收取所需数据。</p>
				<span class="icon mdi mdi-file-document-edit" />
			</div>
			<div class="function">
				<h1>设置</h1>
				<p>编辑用户信息，配置和管理 Monologue 本体的行为和数据处理方式。</p>
				<span class="icon mdi mdi-cog" />
			</div>
			<div class="function">
				<h1>关于 Monologue</h1>
				<p>查看 Monologue 的版本信息、更新日志和更多相关的技术层面内容。</p>
				<span class="icon mdi mdi-information-variant" />
			</div>
		</div>
		<h1>管理</h1>
		<div class="function-group">
			<div class="function">
				<h1>发布管理</h1>
				<p>管理已经发布的事件、投票等项目，对它们进行批量编辑或删除。</p>
				<span class="icon mdi mdi-pencil" />
			</div>
			<div class="function">
				<h1>统计</h1>
				<p>统计访问整个网站或某一页面的用户信息。</p>
				<span class="icon mdi mdi-cursor-default" />
			</div>
			<div class="function">
				<h1>投票结果</h1>
				<p>查看并分析现有投票的结果，并生成第三方格式的表格供下载。</p>
				<span class="icon mdi mdi-chart-donut" />
			</div>
			<div class="function">
				<h1>留言阅读</h1>
				<p>阅读留言区收集到的留言内容，对其进行归档或删除管理。</p>
				<span class="icon mdi mdi-comment-eye" />
			</div>
			<div class="function">
				<h1>问卷反馈</h1>
				<p>查看、评价、归纳问卷的填写和填写者信息，对其进行归档或删除管理。</p>
				<span class="icon mdi mdi-file-check" />
			</div>
		</div>
		<h1>文档</h1>
		<div class="function-group">
			<div class="function">
				<h1>Mono API</h1>
				<p>Monologue 提供的公开 API，使第三方可轻松获得相关数据。</p>
				<span class="icon mdi mdi-web-box" />
			</div>
			<div @click="locate('https://book.sotap.org/#/monologue/index')" class="function" active>
				<h1>开发文档与函数库</h1>
				<p>查看我们在 SoTap Book 上所编写的开发文档，了解 Monologue 的开发过程。</p>
				<span class="icon mdi mdi-file-code" />
			</div>
			<div @click="locate('https://github.com/sotapmc/Monologue')" class="function" active>
				<h1>GitHub 仓库</h1>
				<p>查看我们托管在 GitHub 上的仓库，可以提出问题或者发起 PR，我们欢迎您的到来！</p>
				<span class="icon mdi mdi-github" />
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
import { locate } from '../functions';

export default Vue.extend({
	data() {
		return {
			auth: false,
			snackbar: false,
			snackbarMessage: "",
			logoutConfirmDialog: false,
			logoutConfirmed: false,
			logoutCompleted: false,
			logoutFailed: false
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
							});
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
		},
		locate
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
		opacity: .6;
	}

	.function[active] {
		opacity: 1;
	}

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

h1 {
	padding-top: 16px;
	padding-bottom: 16px;
}

.admin-container {
	margin-bottom: 56px;
}

</style>
