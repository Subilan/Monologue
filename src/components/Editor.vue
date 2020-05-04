<template>
	<div class="editor">
		<md-empty-state v-if="invalid">
			<span class="md-empty-state-icon mdi mdi-help-circle-outline" />
			<span class="md-empty-state-label">无效的页面</span>
			<span class="md-empty-state-description">目标页面不存在或发生了错误</span>
			<md-button @click="$router.go(-1)" class="md-primary md-raised">后退</md-button>
		</md-empty-state>
		<LoadingScreen v-if="loading" />
		<div class="full-height">
			<div class="hero">
				<slot name="hero"></slot>
			</div>
			<FunctionBar class="function-bar-float-right">
				<slot name="toolbar"></slot>
			</FunctionBar>
			<md-field :class="titleInvalid">
				<md-icon class="mdi mdi-format-title" />
				<label>标题</label>
				<md-input v-model="title" type="text" maxlength="30" required />
				<span class="md-error">无效的标题</span>
			</md-field>
			<editor-tool-bar :enabled="pcView" @update-content="content = $event" :content="content">
				<md-field class="content-field" :class="contentInvalid">
					<label>内容</label>
					<md-textarea class="content-input" v-model="content" type="text" maxlength="1000" required />
					<span class="md-helper-text">支持 Markdown 语法。</span>
					<span class="md-error">无效的内容</span>
				</md-field>
			</editor-tool-bar>
			<md-button @click="createSubmitEvent()" class="submit-btn md-primary md-raised">发布</md-button>	
		</div>
	</div>
</template>

<script lang="ts">
import Vue from "vue";
// @ts-ignore
import MdField from "vue-material/dist/components/MdField";
// @ts-ignore
import MdIcon from "vue-material/dist/components/MdIcon";
// @ts-ignore
import MdButton from "vue-material/dist/components/MdButton";
// @ts-ignore
import MdMenu from "vue-material/dist/components/MdMenu";
// @ts-ignore
import MdList from "vue-material/dist/components/MdList";
// @ts-ignore
import MdSnackbar from "vue-material/dist/components/MdSnackbar";
// @ts-ignore
import MdEmptyState from "vue-material/dist/components/MdEmptyState";
// @ts-ignore
import MdDialog from "vue-material/dist/components/MdDialog";
// @ts-ignore
import MdCheckbox from "vue-material/dist/components/MdCheckbox";
import LoadingScreen from "@/components/LoadingScreen.vue";
import FunctionBar from "@/components/FunctionBar.vue";
import EditorToolBar from "@/components/EditorToolBar.vue";
import { isPCView } from "@/functions";

Vue.use(MdField)
	.use(MdIcon)
	.use(MdButton)
	.use(MdMenu)
	.use(MdList)
	.use(MdSnackbar)
	.use(MdEmptyState)
	.use(MdDialog)
	.use(MdCheckbox);

export default Vue.extend({
	props: ["loading", "invalid", "editingTitle", "editingContent"],
	data() {
		return {
			empty: false,
			title: "",
			content: "",
			titleInvalid: "",
			contentInvalid: "",
			pcView: false
		};
	},
	components: {
		LoadingScreen,
		FunctionBar,
		EditorToolBar
	},
	methods: {
		createSubmitEvent() {
			this.$emit("submit", {
				title: this.title,
				content: this.content
			});
		},
		isPCView
	},
	watch: {
		title(v) {
			if (v.length > 0 && v.length <= 30) {
				this.titleInvalid = "";
			} else {
				this.titleInvalid = "md-invalid";
			}
		},
		content(v) {
			if (v.length > 0 && v.length <= 1000) {
				this.contentInvalid = "";
			} else {
				this.contentInvalid = "md-invalid";
			}
		},
		editingTitle(v) {
			this.title = v;
		},
		editingContent(v) {
			this.content = v;
		},
	},
	mounted() {
		this.pcView = this.isPCView();

		window.onbeforeunload = e => {
			if (this.$route.name === "admin-new-event" || this.$route.name === "admin-edit-event") {
				e = e || window.event;
				if (e) {
					e.returnValue = "是否确实要离开此页面？您的修改将不会被保存。";
				}
				return "是否确实要离开此页面？您的修改将不会被保存。";
			} else {
				window.onbeforeunload = null;
			}
		};
	}
});
</script>

<style lang="less" scoped>
.editor {
	height: 100%;
	position: relative;

	.content-field {
        @media screen and (max-width: 1024px) {
            height: 100%;
        }
        @media screen and (min-width: 1024px) {
            height: calc(100% - 68px);
        }
		position: relative;

		.content-input {
			height: 100%;
		}
	}

	.submit-btn-container {
		width: 100%;
		.submit-btn {
			display: block;
			margin: auto;
		}
	}
}

.full-height {
	@media screen and (max-width: 1024px) {
		height: 100% !important;
	}
	position: relative;
}
</style>
