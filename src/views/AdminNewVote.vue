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
						<md-input type="text" v-model="voteData[k - 1]" />
					</md-field>
					<md-button v-if="k > 1" @click="deleteVoteItem(k - 1)" class="md-icon-button md-primary">
						<md-icon class="mdi mdi-close" />
					</md-button>
				</div>
				<md-button v-if="k === voteItemCount && k !== maxVoteItemCount" @click="duplicateVoteItem()" class="create-vote-item md-button"><md-icon class="mdi mdi-plus-circle" /> 新增投票项</md-button>
			</div>
		</div>
		<md-snackbar :md-active.sync="snackbar" md-position="center" :md-duration="1500" md-persistent>{{ snackbarMessage }}</md-snackbar>
		<md-dialog :md-active.sync="deleteConfirmDialog">
			<md-dialog-title>删除确认</md-dialog-title>
			<md-dialog-content>是否要确认删除此协议？此操作无法回滚。</md-dialog-content>
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
	</div>
</template>

<script lang="ts">
import Vue from "vue";
import PageHeader from "@/components/PageHeader.vue";
// @ts-ignore
import MdField from "vue-material/dist/components/MdField";
// @ts-ignore
import MdCheckbox from "vue-material/dist/components/MdCheckbox";

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
			multipleMaxCount: 2
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
			if (!Number.isNaN(Number(v)) && v >= 2 && v <= this.voteItemCount) {
				this.multipleMaxCountInvalid = "";
			} else {
				this.multipleMaxCountInvalid = "md-invalid";
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
			delete this.voteData[index];
			if (this.multipleMaxCount === this.voteItemCount) {
				this.multipleMaxCount -= 1;
			}
			this.voteItemCount -= 1;
			console.log("after:", this.voteData, this.multipleMaxCount, this.voteItemCount);
		}
	},
	mounted() {}
});
</script>

<style lang="less" scoped>
.vote-editor {
	.mdui-shadow-2;
	border-radius: 2px;
	padding: 16px;
	margin-top: 56px;

	.vote-item {
		.create-vote-item {
			width: calc(100% - 16px);

			.mdi {
				margin-right: 8px;
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
