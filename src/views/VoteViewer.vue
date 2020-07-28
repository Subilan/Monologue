<template>
	<div class="vote-viewer full-height">
		<div class="vote-container">
			<page-header class="no-padding" :functionbar="false">
				<h1>{{ title }}</h1>
				<span v-html="description" />
			</page-header>
			<div class="vote-content-container">
				<div class="vote-single" v-if="!multiple">
					<md-radio class="no-selection" :disabled="duplicatedVote" v-for="(k, i) in items" :key="i" v-model="selected" :value="i">
						{{ k }}
					</md-radio>
				</div>
				<div class="vote-multiple" v-if="multiple">
					<md-checkbox class="no-selection" :disabled="multipleDisabled[i] || duplicatedVote" v-for="(k, i) in items" :key="i" v-model="multipleSelected[i]">
						{{ k }}
					</md-checkbox>
				</div>
			</div>
			<md-snackbar :md-active.sync="snackbar" md-position="center" :md-duration="1500" md-persistent>{{ snackbarMessage }}</md-snackbar>
			<md-button :disabled="duplicatedVote" @click="submitDialog = true" class="center md-primary md-raised">提交</md-button>
			<md-dialog :md-active.sync="submitDialog">
				<md-dialog-title>提交确认</md-dialog-title>
				<md-dialog-content>
					是否确认提交投票？此操作不可撤销且<strong>无法修改</strong>。
				</md-dialog-content>
				<md-dialog-actions>
					<md-button class="md-primary" @click="submitDialog = false">取消</md-button>
					<md-button
						class="md-primary md-raised"
						@click="
							submit();
							submitDialog = false;
						"
						>提交</md-button
					>
				</md-dialog-actions>
			</md-dialog>
			<md-dialog :md-active.sync="loadingDialog">
				<md-dialog-content>
					<loading-screen />
				</md-dialog-content>
			</md-dialog>
		</div>
	</div>
</template>

<script lang="ts">
import Vue from "vue";
import PageHeader from "@/components/PageHeader.vue";
// @ts-ignore
import MdCheckbox from "vue-material/dist/components/MdCheckbox";
// @ts-ignore
import MdRadio from "vue-material/dist/components/MdRadio";
import { fillArray, getDuplicatedCount } from "../functions";
import LoadingScreen from "@/components/LoadingScreen.vue";

Vue.use(MdCheckbox).use(MdRadio);

export default Vue.extend({
	data() {
		return {
			title: "",
			description: "",
			date: "",
			multiple: false,
			multipleMaxCount: -1,
			items: [],
			data: [],
			selected: -1,
			multipleSelected: [] as Array<boolean>,
			multipleDisabled: [] as Array<boolean>,
			submitDialog: false,
			snackbar: false,
			snackbarMessage: "",
			disableSubmit: false,
			loadingDialog: false,
			duplicatedVote: true,
		};
	},
	components: {
		PageHeader,
		LoadingScreen
	},
	created() {
		this.loadingDialog = true;
		if (!Number.isInteger(Number(this.$route.params.id))) {
			this.$router.push({
				name: "error-not-found"
			});
		}
		this.$server.post(
			"/api/vote",
			{
				method: "duplicated",
				id: this.$route.params.id
			},
			r => {
				if (r.data) {
					let data = r.data;
					let selection: Array<number> = JSON.parse(data.selection);
					this.duplicatedVote = true;
					if (selection.length === 1) {
						this.selected = selection[0];
					} else {
						selection.forEach(k => {
							this.$set(this.multipleSelected, k, true)
						})
					}
				} else {
					this.duplicatedVote = false;
				}
			}
		);
		this.$server.get("/api/vote?id=" + this.$route.params.id + "&markdown=true", r => {
			this.loadingDialog = false;
			if (r.data) {
				let data = r.data;
				let multiple = Number(data.multiple);
				this.title = data.title;
				this.description = data.description;
				this.multiple = multiple >= 2;
				this.multipleMaxCount = multiple;
				this.date = data.date.split(" ")[0];
				this.items = JSON.parse(data.items);
				if (this.multiple) {
					// initialize multiple data array
					this.multipleDisabled = fillArray(this.multipleDisabled, false, this.items.length);
					this.multipleSelected = fillArray(this.multipleSelected, false, this.items.length);
					this.$watch("multipleSelected", v => {
						if (getDuplicatedCount(v).true >= this.multipleMaxCount) {
							this.multipleDisabled = this.multipleSelected.map(k => !k);
						} else {
							this.multipleDisabled = fillArray(this.multipleDisabled, false, this.items.length, true);
						}
					});
				}
			} else {
				this.$router.push({
					name: "error-not-found"
				})
			}
		});
	},
	methods: {
		submit() {
			if (this.disableSubmit) {
				return false;
			}
			if (!this.verify()) {
				this.snackbarMessage = "您必须选择至少一项才可提交";
				this.snackbar = true;
				return false;
			}
			if (this.duplicatedVote) {
				this.snackbarMessage = "不能重复提交投票";
				this.snackbar = true;
				return false;
			}
			this.loadingDialog = true;
			this.$server.post(
				"/api/vote",
				{
					method: "update",
					id: this.$route.params.id,
					multiple: this.multiple,
					data: this.getData()
				},
				r => {
					this.loadingDialog = false;
					if (r.data) {
						this.snackbarMessage = "成功提交投票信息，即将为您跳转";
						this.disableSubmit = true;
						this.snackbar = true;
						setTimeout(() => {
							this.$router.push({
								name: "home"
							});
						}, 1500);
					} else {
						this.snackbarMessage = "投票失败，内部错误";
						this.snackbar = true;
					}
				}
			);
		},
		getData() {
			let arr: Array<number> = [];
			if (this.multiple) {
				let copy = this.multipleSelected;
				copy.forEach((k, i) => {
					if (k) {
						arr.push(i);
					}
				});
			} else {
				arr.push(this.selected);
			}
			return arr;
		},
		verify() {
			let data = this.getData();
			return !data.includes(-1) && data.length > 0;
		}
	},
	mounted() {}
});
</script>

<style lang="less" scoped>
.vote-content-container {
	.vote-single,
	.vote-multiple {
		display: grid;

		> * {
			z-index: 1;
		}
	}

	> * {
		font-size: 20px;
	}
}

.vote-viewer {
	display: flex;
	align-items: center;

	.vote-container {
		.outlined;
		width: 100%;
		padding: 32px;

		.md-primary.md-raised {
			margin-top: 32px;
		}
	}
}
</style>
