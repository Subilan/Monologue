<template>
	<div class="admin-vote admin-container">
		<page-header>
			<h1>创建投票</h1>
			<p>以可视化的方式创建一个新的数据收集实例</p>
			<template v-slot:functions>
				<md-button v-if="editing" @click="deleteConfirmDialog = true" class="md-icon-button md-raised">
					<md-icon class="mdi mdi-delete" />
				</md-button>
				<md-button @click="$router.push({ name: 'admin-panel' })" class="md-icon-button md-raised">
					<md-icon class="mdi mdi-cogs" />
				</md-button>
				<md-button @click="configurationDialog = true" class="md-icon-button md-raised">
					<md-icon class="mdi mdi-card-bulleted" />
				</md-button>
				<md-button v-if="maxVoteItemCount - voteItemCount >= 2" @click="createMultipleDialog = true" class="md-icon-button md-raised">
					<md-icon class="mdi mdi-plus-circle-multiple"/>
				</md-button>
				<md-button @click="submit()" class="md-icon-button md-primary md-raised">
					<md-icon class="mdi mdi-send" />
				</md-button>
			</template>
		</page-header>
		<md-field :class="titleInvalid">
			<md-icon class="mdi mdi-format-title" />
			<label>标题</label>
			<md-input v-model="title" maxlength="30" type="text" />
			<span class="md-helper-text">投票的标题</span>
			<span class="md-error">无效的标题</span>
		</md-field>
		<md-field :class="descriptionInvalid">
			<md-icon class="mdi mdi-card-text" />
			<label>介绍</label>
			<md-input v-model="description" maxlength="100" type="text" />
			<span class="md-helper-text">选填，针对该投票的一段介绍</span>
			<span class="md-error">无效的介绍</span>
		</md-field>
		<div class="vote-editor">
			<div class="vote-item" v-for="k in voteItemCount" :key="k">
				<div class="vote-item-inner">
					<md-field class="vote-field">
						<label>投票项</label>
						<md-input @keyup.enter="duplicateVoteItem()" type="text" v-model="voteData[k - 1]" />
					</md-field>
					<md-button v-if="k > 1" @click="deleteVoteItem(k - 1)" class="md-icon-button md-primary">
						<md-icon class="mdi mdi-close" />
					</md-button>
				</div>
				<div v-if="k === voteItemCount" class="actions">
					<md-button v-if="k !== maxVoteItemCount" @click="duplicateVoteItem()">
						<md-icon class="mdi mdi-plus-circle" /> 新增投票项
					</md-button>
				</div>
			</div>
			<small> 已添加 {{ voteItemCount }} / {{ maxVoteItemCount }} 个 </small>
		</div>
		<md-snackbar :md-active.sync="snackbar" md-position="center" :md-duration="1500" md-persistent>{{ snackbarMessage }}</md-snackbar>
		<md-dialog :md-active.sync="deleteConfirmDialog">
			<md-dialog-title>删除确认</md-dialog-title>
			<md-dialog-content>是否要确认删除此投票？该投票以及其数据将永久丢失。</md-dialog-content>
			<md-dialog-actions>
				<md-button
					@click="
						deleteVote();
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
				<md-checkbox :disabled="voteItemCount < 2" v-model="multipleVote">
					允许多选
				</md-checkbox>
				<md-field v-if="multipleVote && voteItemCount > 2" :class="multipleMaxCountInvalid">
					<md-icon class="mdi mdi-format-vertical-align-top" />
					<label>最多可选...</label>
					<md-input v-model="multipleMaxCount" type="number" step="1" min="2" :max="voteItemCount" />
					<span class="md-helper-text">不大于 {{ voteItemCount }} 的整数</span>
					<span class="md-error">无效的数字</span>
				</md-field>
			</md-dialog-content>
			<md-dialog-actions>
				<md-button class="md-primary md-raised" @click="configurationDialog = false">OK</md-button>
			</md-dialog-actions>
		</md-dialog>
		<md-dialog :md-active.sync="createMultipleDialog">
			<md-dialog-title>批量创建</md-dialog-title>
			<md-dialog-content>
				<md-field :class="createMultipleCountInvalid">
					<md-icon class="mdi mdi-plus-circle-multiple" />
					<label>创建个数</label>
					<md-input v-model="createMultipleCount" type="number" step="1" min="2" :max="maxVoteItemCount - voteItemCount" />
					<span class="md-helper-text">不大于 {{ maxVoteItemCount - voteItemCount }} 的整数</span>
					<span class="md-error">无效的数字</span>
				</md-field>
			</md-dialog-content>
			<md-dialog-actions>
				<md-button class="md-primary" @click="createMultipleDialog = false">取消</md-button>
				<md-button
					class="md-primary md-raised"
					@click="
						createMultiple();
						createMultipleDialog = false;
					"
					>创建</md-button
				>
			</md-dialog-actions>
		</md-dialog>
	</div>
</template>

<script lang="ts">
import Vue from "vue";
import PageHeader from "@/components/PageHeader.vue";
// @ts-ignore
import MdField from "vue-material/dist/components/MdField";
// @ts-ignore
import MdCheckbox from "vue-material/dist/components/MdCheckbox";
import { isNumericString } from "@/functions";

Vue.use(MdField).use(MdCheckbox);

export default Vue.extend({
	data() {
		return {
			editing: false,
			deleteConfirmDialog: false,
			configurationDialog: false,
			snackbar: false,
			snackbarMessage: "",
			titleInvalid: "",
			title: "",
			descriptionInvalid: "",
			description: "",
			voteItemCount: 1,
			incrementDisabled: false,
			maxVoteItemCount: 20,
			voteData: [],
			multipleVote: false,
			multipleMaxCountInvalid: "",
			multipleMaxCount: 2,
			createMultipleDialog: false,
			createMultipleCount: 2,
			createMultipleCountInvalid: ""
		};
	},
	components: {
		PageHeader
	},
	watch: {
		title(v) {
			if (v.length > 0 && v.length <= 30) {
				this.titleInvalid = "";
			} else {
				this.titleInvalid = "md-invalid";
			}
		},
		description(v) {
			if (v.length >= 0 && v.length <= 100) {
				this.descriptionInvalid = "";
			} else {
				this.descriptionInvalid = "md-invalid";
			}
		},
		voteItemCount(v) {
			if (v > this.maxVoteItemCount) {
				this.incrementDisabled = true;
			}
		},
		multipleMaxCount(v) {
			if (isNumericString(v) && v >= 2 && v <= this.voteItemCount) {
				this.multipleMaxCountInvalid = "";
			} else {
				this.multipleMaxCountInvalid = "md-invalid";
			}
		},
		createMultipleCount(v) {
			if (isNumericString(v) && v >= 2 && v <= this.maxVoteItemCount - this.voteItemCount) {
				this.createMultipleCountInvalid = "";
			} else {
				this.createMultipleCountInvalid = "md-invalid";
			}
		}
	},
	methods: {
		duplicateVoteItem() {
			if (!this.incrementDisabled) {
				this.voteItemCount++;
			} else {
				return false;
			}
		},
		deleteVoteItem(index) {
			console.log("before:", this.voteData, this.multipleMaxCount, this.voteItemCount);
			this.voteData.splice(index, 1);
			if (this.multipleMaxCount === this.voteItemCount) {
				this.multipleMaxCount -= 1;
			}
			this.voteItemCount -= 1;
			console.log("after:", this.voteData, this.multipleMaxCount, this.voteItemCount);
		},
		createMultiple() {
			let count = Number(this.createMultipleCount);
			let num = Number(this.voteItemCount);
			// this.voteItemCount += count causes duplicate key error here.
			// this.voteItemCount will be updated wrongly as a string value but not number value through this.
			if (count + num <= this.maxVoteItemCount && count > 0) {
				if (count >= 2) {
					this.voteItemCount = num + count;
				} else {
					this.snackbarMessage = "这似乎并不是批量创建";
					this.snackbar = true;
				}
			} else {
				this.snackbarMessage = "无法批量创建，数量超过限制";
				this.snackbar = true;
			}
		},
		submit() {
			console.log(JSON.stringify(this.voteData));
			this.$server.post("/api/vote", {
				method: "create",
				title: this.title,
				desc: this.description,
				items: JSON.stringify(this.voteData),
				multiple: this.multipleVote ? this.multipleMaxCount : -1
			}, r => {
				console.log(r);
			})
		}
	},
	mounted() {}
});
</script>

<style lang="less" scoped>
.vote-editor {
	.outlined;
	border-radius: 2px;
	padding: 16px;
	margin-top: 56px;
	margin-bottom: 56px;

	.vote-item {
		.actions {
			width: calc(100% - 16px);
			position: relative;
			margin-top: 16px;
			margin-bottom: 16px;

			.md-button {
				width: 100%;

				.mdi {
					margin-right: 8px;
				}
			}
		}

		.vote-item-inner {
			display: flex;
			align-items: center;

			.number {
				font-weight: bold;
			}
		}
	}
}
</style>