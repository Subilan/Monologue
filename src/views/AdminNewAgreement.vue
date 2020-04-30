<template>
    <div class="admin-agreement">
        <md-empty-state v-if="invalidID">
            <span class="md-empty-state-icon mdi mdi-help-circle-outline" />
            <span class="md-empty-state-label">无效的 ID</span>
            <span class="md-empty-state-description">您输入的 ID 有误或者不存在</span>
            <md-button @click="$router.go(-1)" class="md-primary md-raised">后退</md-button>
        </md-empty-state>
        <LoadingScreen v-if="loading" />
        <div class="full-height" v-if="!isEdit()">
            <div class="hero">
                <h1>创建协议</h1>
                <p>创建协议并收集同意或不同意协议的人员。</p>
            </div>
            <FunctionBar class="function-bar-float-right">
                <md-checkbox v-model="allowDisagreement" class="md-primary">允许反对意见</md-checkbox>
                <md-button
                    @click="$router.push({name: 'admin-panel'})"
                    class="md-icon-button md-raised"
                >
                    <md-icon class="mdi mdi-cogs" />
                </md-button>
            </FunctionBar>
            <md-field :class="titleInvalid">
                <md-icon class="mdi mdi-format-title" />
                <label>协议标题</label>
                <md-input v-model="title" type="text" maxlength="40" required />
                <span class="md-error">无效的标题</span>
            </md-field>
            <md-field class="agreement-content" :class="contentInvalid">
                <label>内容</label>
                <md-textarea
                    class="agreement-content-input"
                    v-model="content"
                    type="text"
                    maxlength="1000"
                    required
                />
                <span class="md-helper-text">协议的内容，支持 Markdown 语法。</span>
                <span class="md-error">无效的内容</span>
            </md-field>
            <md-button class="submit-btn md-primary md-raised">发布</md-button>
        </div>
        <md-dialog :md-active.sync="routerConfirmDialog">
            <md-dialog-title>跳转确认</md-dialog-title>
            <md-dialog-content>是否确认要跳转到其它页面？未保存的更改将永久消失。</md-dialog-content>
            <md-dialog-actions>
                <md-button @click="next(); routerConfirmDialog = false" class="md-primary">跳转</md-button>
                <md-button @click="routerConfirmDialog = false" class="md-primary md-raised">取消</md-button>
            </md-dialog-actions>
        </md-dialog>
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
    data() {
        return {
            titleInvalid: "",
            contentInvalid: "",
            title: "",
            content: "",
            invalidID: false,
            loading: false,
            allowDisagreement: false,
            routerConfirmDialog: false,
            actioned: false,
            next: () => {}
        };
    },
    methods: {
        isEdit() {
            return this.$route.name === "admin-edit-agreement";
        }
    },
    watch: {
        title(v) {
            if (v.length > 0 && v.length < 40) {
                this.titleInvalid = "";
            } else {
                this.titleInvalid = "md-invalid";
            }
        },
        content(v) {
            if (v.length > 0 && v.length < 1000) {
                this.contentInvalid = "";
            } else {
                this.contentInvalid = "md-invalid";
            }
        }
    },
    components: {
        LoadingScreen,
        FunctionBar
    },
    mounted() {
        window.onbeforeunload = e => {
            if (
                (this.$route.name === "admin-new-agreement" ||
                    this.$route.name === "admin-edit-agreement") &&
                (this.title.length > 0 || this.content.length > 0)
            ) {
                e = e || window.event;
                if (e) {
                    e.returnValue =
                        "是否确实要离开此页面？您的修改将不会被保存。";
                }
                return "是否确实要离开此页面？您的修改将不会被保存。";
            } else {
                window.onbeforeunload = null;
            }
        };
    },
    beforeRouteLeave(to, from, next) {
        if (
            (this.title.length > 0 || this.content.length > 0) &&
            !this.actioned
        ) {
            this.next = next;
            this.routerConfirmDialog = true;
            next(false);
        } else {
            next();
        }
    }
});
</script>

<style lang="less" scoped>
.admin-agreement {
    height: 100%;
    position: relative;
    padding: 16px;
    padding-bottom: 0;
    .agreement-content {
        height: 70% !important;
        position: relative;
        .agreement-content-input {
            height: 100% !important;
            position: relative;
        }
    }
}
</style>