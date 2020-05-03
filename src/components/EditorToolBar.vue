<template>
	<div class="editor-toolbar-container">
		<div class="editor-toolbar" v-if="enabled">
			<md-button @click="createFormat('bold')" class="item md-raised md-icon-button">
				<md-icon class="mdi mdi-format-bold" />
			</md-button>
			<md-button @click="createFormat('italic')" class="item md-raised md-icon-button">
				<md-icon class="mdi mdi-format-italic" />
			</md-button>
			<md-button @click="createFormat('underline')" class="item md-raised md-icon-button">
				<md-icon class="mdi mdi-format-underline" />
			</md-button>
			<div class="vertical-divider" />
			<md-menu md-size="big" md-direction="bottom-end" :mdCloseOnSelect="true" :mdCloseOnClick="true">
				<md-button class="md-icon-button md-raised" md-menu-trigger>
					<md-icon class="mdi mdi-format-header-pound" />
				</md-button>

				<md-menu-content>
					<md-menu-item @click="createFormat('header' + i)" v-for="i in 6" :key="i">
						<span>{{ translateNumber(i) }}级标题</span>
						<md-icon class="mdi" :class="'mdi-format-header-' + i" />
					</md-menu-item>
				</md-menu-content>
			</md-menu>
			<md-button @click="createFormat('blockquote')" class="item md-raised md-icon-button">
				<md-icon class="mdi mdi-format-quote-close" />
			</md-button>
			<md-button @click="createFormat('strikethrough')" class="item md-raised md-icon-button">
				<md-icon class="mdi mdi-format-strikethrough" />
			</md-button>
			<md-button @click="createFormat('codeblock')" class="item md-raised md-icon-button">
				<md-icon class="mdi mdi-code-tags" />
			</md-button>
			<div class="vertical-divider" />
			<md-button @click="insertImageDialog = true" class="item md-raised md-icon-button">
				<md-icon class="mdi mdi-image" />
			</md-button>
			<md-button @click="insertLinkDialog = true" class="item md-raised md-icon-button">
				<md-icon class="mdi mdi-link" />
			</md-button>
		</div>
		<md-dialog :md-active.sync="insertImageDialog">
			<md-dialog-title>插入图片</md-dialog-title>
			<md-dialog-content>
				<md-field>
					<md-icon class="mdi mdi-tag" />
					<label>图片标题</label>
					<md-input type="text" v-model="textareaValue1" />
				</md-field>
				<md-field>
					<md-icon class="mdi mdi-image" />
					<label>图片链接</label>
					<md-input type="text" v-model="textareaValue2" />
				</md-field>
			</md-dialog-content>
			<md-dialog-actions>
				<md-button class="md-primary" @click="insertImageDialog = false">取消</md-button>
				<md-button
					class="md-primary md-raised"
					@click="
						insertData('image', textareaValue1, textareaValue2);
						insertImageDialog = false;
					"
					>插入</md-button
				>
			</md-dialog-actions>
		</md-dialog>
		<md-dialog :md-active.sync="insertLinkDialog">
			<md-dialog-title>插入链接</md-dialog-title>
			<md-dialog-content>
				<md-field>
					<md-icon class="mdi mdi-tag" />
					<label>显示文字</label>
					<md-input type="text" v-model="textareaValue1" />
				</md-field>
				<md-field>
					<md-icon class="mdi mdi-link" />
					<label>链接地址</label>
					<md-input type="text" v-model="textareaValue2" />
				</md-field>
			</md-dialog-content>
			<md-dialog-actions>
				<md-button class="md-primary" @click="insertLinkDialog = false">取消</md-button>
				<md-button
					class="md-primary md-raised"
					@click="
						insertData('link', textareaValue1, textareaValue2);
						insertLinkDialog = false;
					"
					>插入</md-button
				>
			</md-dialog-actions>
		</md-dialog>
		<slot class="textfield"></slot>
	</div>
</template>

<script lang="ts">
import Vue from "vue";
// @ts-ignore
import MdButton from "vue-material/dist/components/MdButton";
// @ts-ignore
import MdIcon from "vue-material/dist/components/MdIcon";
// @ts-ignore
import MdTooltip from "vue-material/dist/components/MdTooltip";
// @ts-ignore
import MdMenu from "vue-material/dist/components/MdMenu";
// @ts-ignore
import MdDialog from "vue-material/dist/components/MdDialog";
// @ts-ignore
import MdField from "vue-material/dist/components/MdField";
import { translateNumber, isNumericStringBetween } from "@/functions";

Vue.use(MdButton)
	.use(MdIcon)
	.use(MdTooltip)
	.use(MdMenu)
	.use(MdDialog)
	.use(MdField);

type FormatNames = "bold" | "italic" | "underline" | "header1" | "header2" | "header3" | "header4" | "header5" | "header6" | "blockquote" | "strikethrough" | "codeblock";

export default Vue.extend({
	props: ["content", "enabled"],
	data() {
		return {
			textarea: null,
			imageLink: "",
			link: "",
			insertImageDialog: false,
			insertLinkDialog: false,
			textareaValue1: "",
			textareaValue2: ""
		};
	},
	methods: {
		translateNumber,
		handleSelection(start: number, end: number) {
			// @ts-ignore
			let textarea: HTMLTextAreaElement = this.$slots.default[0].elm.children[1];
			textarea.setSelectionRange(start, end);
			textarea.focus();
		},
		createFormat(name: FormatNames) {
			let content = this.content;
			let beforeLength = content.length;
			let match = {
				bold: "**粗体**",
				italic: "**斜体**",
				underline: "<u>下划线</u>",
				header1: "\n# 一级标题",
				header2: "\n## 二级标题",
				header3: "\n### 三级标题",
				header4: "\n#### 四级标题",
				header5: "\n##### 五级标题",
				header6: "\n###### 六级标题",
				blockquote: "\n\n> 引用文本",
				strikethrough: "~~删除文本~~",
				codeblock: "`代码块`"
			};
			let posMatch = {
				bold: [2, 2],
				italic: [2, 2],
				underline: [3, 3],
				header1: [3, 4],
				header2: [4, 4],
				header3: [5, 4],
				header4: [6, 4],
				header5: [7, 4],
				header6: [8, 4],
				blockquote: [4, 4],
				strikethrough: [2, 4],
				codeblock: [1, 3]
			};
			let newcontent = content + match[name];
			let pos = posMatch[name];
			let afterLength = content.length;
			this.$emit("update-content", newcontent);
			this.$nextTick(() => {
				this.handleSelection(beforeLength + pos[0], beforeLength + pos[1] + pos[0]);
			});
		},
		insertData(type: string, arg1: string, arg2: string) {
			let content = this.content;
			if (arg2.length > 0) {
				switch (type) {
					case "image":
						content += "![" + arg1 + "](" + arg2 + ")";
						break;

					case "link":
						content += "[" + arg1 + "](" + arg2 + ")";
						break;
				}
				this.$emit("update-content", content);
			}
		}
	},
	mounted() {
		window.addEventListener("keydown", e => {
			let key = e.keyCode;
			if (e.ctrlKey) {
				if (e.shiftKey) {
					switch (key) {
						// L
						case 76:
							e.preventDefault();
							this.insertLinkDialog = true;
							break;

						// I
						case 73:
							e.preventDefault();
							this.insertImageDialog = true;
							break;
					}
				} else {
					switch (key) {
						// B
						case 66:
							e.preventDefault();
							this.createFormat("bold");
							break;

						// I
						case 73:
							e.preventDefault();
							this.createFormat("italic");
							break;

						// U
						case 85:
							e.preventDefault();
							this.createFormat("underline");
							break;
						// Q
						case 81:
							e.preventDefault();
							this.createFormat("blockquote");
							break;

						// D
						case 68:
							e.preventDefault();
							this.createFormat("strikethrough");
							break;

						// K
						case 75:
							e.preventDefault();
							this.createFormat("codeblock");
							break;

						default:
							// 1 ~ 6
							if (key >= 49 && key <= 54) {
								e.preventDefault();
								// @ts-ignore
								this.createFormat("header" + (key - 48).toString())
							}
							break;
					}
				}
			}
		});
	}
});
</script>

<style lang="less" scoped>
.editor-toolbar {
	display: flex;
	align-items: center;
	flex-wrap: nowrap;
	padding-top: 14px;
	padding-bottom: 14px;

	> * {
		display: block;
		margin-left: 8px;
		margin-right: 8px;

		&:first-child {
			margin-left: 0;
		}

		&:last-child {
			margin-right: 0;
		}
	}
}

.editor-toolbar-container {
	@media screen and (min-width: 1024px){
		height: calc(60% + 68px);
	}
	@media screen and (max-width: 1024px) {
		height: 60%;
	} 
	position: relative;
}
</style>
