<template>
	<div class="vote-viewer full-height">
		<div class="vote-container">
			<page-header class="no-padding" :functionbar="false">
				<h1>{{ title }}</h1>
				<span v-html="description" />
			</page-header>
			<div class="vote-content-container">
				<md-radio v-for="(k, i) in items" :key="i" v-model="selected" :value="i">
					{{ k }}
				</md-radio>
			</div>
            <md-button @click="submitDialog = true" class="center md-primary md-raised">提交</md-button>
            <md-dialog :md-active.sync="submitDialog">
                <md-dialog-title>提交确认</md-dialog-title>
                <md-dialog-content>
                    是否确认提交投票？此操作不可撤销且<strong>无法修改</strong>。
                </md-dialog-content>
                <md-dialog-actions>
                    <md-button class="md-primary" @click="submitDialog = false">取消</md-button>
                    <md-button class="md-primary md-raised" @click="submit()">提交</md-button>
                </md-dialog-actions>
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
            submitDialog: false,
		};
	},
	components: {
		PageHeader
	},
	created() {
		this.$server.get("/api/vote?id=" + this.$route.params.id + "&markdown=true", r => {
			if (r.data) {
				let data = r.data;
				let multiple = Number(data.multiple);
				this.title = data.title;
				this.description = data.description;
				this.multiple = multiple >= 2;
				this.multipleMaxCount = multiple;
				this.date = data.date.split(" ")[0];
				this.items = JSON.parse(data.items);
			} else {
				this.$router.push({
					name: "error-not-found"
				});
			}
		});
	},
	mounted() {}
});
</script>

<style lang="less" scoped>
.vote-content-container {
	display: grid;

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
