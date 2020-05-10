<template>
	<div class="editor">
		<LoadingScreen v-if="loading" />
		<div class="full-height">
			<page-header>
				<slot name="hero" />
				<template #functions>
					<slot name="toolbar"></slot>
				</template>
				<template #default-functions>
					<md-button @click="createSubmitEvent()" class="submit-btn md-icon-button md-primary md-raised">
						<md-icon class="mdi mdi-send"/>
					</md-button>
				</template>
			</page-header>
			<md-field :class="titleInvalid">
				<md-icon class="mdi mdi-format-title" />
				<label>标题</label>
				<md-input v-model="title" type="text" maxlength="30" required />
				<span class="md-error">无效的标题</span>
			</md-field>
			<editor-tool-bar :enabled="pcView" @update-content="content = $event" :content="content">
				<md-field class="content-field" :class="contentInvalid">
					<label>内容</label>
					<md-textarea @keydown.enter="createSubmitEvent()" class="content-input" v-model="content" type="text" maxlength="1000" required />
					<span class="md-helper-text">支持 Markdown 语法。</span>
					<span class="md-error">无效的内容</span>
				</md-field>
			</editor-tool-bar>
		</div>
	</div>
</template>

<script lang="ts">
import Vue from "vue";
// @ts-ignore
import MdField from "vue-material/dist/components/MdField";
// @ts-ignore
import MdMenu from "vue-material/dist/components/MdMenu";
// @ts-ignore
import MdList from "vue-material/dist/components/MdList";
// @ts-ignore
import MdEmptyState from "vue-material/dist/components/MdEmptyState";
// @ts-ignore
import MdCheckbox from "vue-material/dist/components/MdCheckbox";
import LoadingScreen from "@/components/LoadingScreen.vue";
import PageHeader from "@/components/PageHeader.vue";
import EditorToolBar from "@/components/EditorToolBar.vue";
import { isPCView } from "@/functions";

Vue.use(MdField)
	.use(MdMenu)
	.use(MdList)
	.use(MdEmptyState)
	.use(MdCheckbox);

export default Vue.extend({
	props: ["loading", "editingTitle", "editingContent"],
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
		PageHeader,
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
		}
	},
	mounted() {
		this.pcView = this.isPCView();
		window.onbeforeunload = e => {
			if (this.$store.state.editorCommited === false && this.$route.matched[0].name === "admin-editor") {
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
	.full-height;

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
	}
}
</style>
