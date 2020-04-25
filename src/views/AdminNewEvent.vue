<template>
  <div class="admin-event admin-container">
    <md-empty-state v-if="invalidID">
      <span class="md-empty-state-icon mdi mdi-help-circle-outline" />
      <span class="md-empty-state-label">无效的 ID</span>
      <span class="md-empty-state-description">您输入的 ID 有误或者不存在</span>
      <md-button @click="$router.go(-1)" class="md-primary md-raised">后退</md-button>
    </md-empty-state>
    <div class="full-height" v-if="!isEdit() || !invalidID">
      <div class="hero">
        <h1>{{ isEdit() ? "编辑事件 #" + id : "添加新事件"}}</h1>
        <p>{{ isEdit() ? "修改该事件的内容和相关属性。" : "在时间线上添加新的事件以供外部参考。" }}</p>
      </div>
      <div v-if="isEdit()" class="functions">
        <md-button @click="deleteConfirmDialog = true" class="md-icon-button md-raised">
          <md-icon class="mdi mdi-delete" />
        </md-button>
      </div>
      <div class="new-event-form full-height">
        <md-field :class="titleInvalid">
          <md-icon class="mdi mdi-format-title" />
          <label>事件标题</label>
          <md-input type="text" v-model="title" maxlength="40" required />
          <span class="md-helper-text">不能超过 40 字。</span>
          <span class="md-error">长度无效</span>
        </md-field>
        <md-field class="textarea" :class="contentInvalid">
          <label>事件内容</label>
          <md-textarea type="text" v-model="content" maxlength="1000" required />
          <span class="md-helper-text">支持 Markdown 语法，不能超过 1000 字。</span>
          <span class="md-error">长度无效</span>
        </md-field>
        <md-field>
          <md-icon class="mdi" :class="getIconByType()" />
          <label>选择事件类型</label>
          <md-select required v-model="type">
            <md-option value="info">一般</md-option>
            <md-option value="warning">警告</md-option>
            <md-option value="solved">已解决</md-option>
          </md-select>
        </md-field>
        <md-button @click="submit()" class="submit-btn md-primary md-raised">提交</md-button>
        <md-snackbar
          :md-active.sync="snackbar"
          md-position="center"
          :md-duration="1500"
          md-persistent
        >{{ snackbarMessage }}</md-snackbar>
        <md-dialog :md-active.sync="deleteConfirmDialog">
          <md-dialog-title>删除确认</md-dialog-title>
          <md-dialog-content>是否要确认删除此事件？此操作无法回滚。</md-dialog-content>
          <md-dialog-actions>
            <md-button @click="deleteEvent(); deleteConfirmDialog = false" class="md-primary">确认删除</md-button>
            <md-button @click="deleteConfirmDialog = false" class="md-primary md-raised">取消</md-button>
          </md-dialog-actions>
        </md-dialog>
        <md-dialog :md-active.sync="routerConfirmDialog">
          <md-dialog-title>跳转确认</md-dialog-title>
          <md-dialog-content>是否确认要跳转到其它页面？未保存的更改将永久消失。</md-dialog-content>
          <md-dialog-actions>
            <md-button @click="next(); routerConfirmDialog = false" class="md-primary">跳转</md-button>
            <md-button @click="routerConfirmDialog = false" class="md-primary md-raised">取消</md-button>
          </md-dialog-actions>
        </md-dialog>
      </div>
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

Vue.use(MdField)
  .use(MdIcon)
  .use(MdButton)
  .use(MdMenu)
  .use(MdList)
  .use(MdSnackbar)
  .use(MdEmptyState)
  .use(MdDialog);

export default Vue.extend({
  data() {
    return {
      title: "",
      content: "",
      type: "info",
      id: -1,
      titleInvalid: "",
      contentInvalid: "",
      snackbar: false,
      snackbarMessage: "",
      disableSubmit: false,
      invalidID: false,
      deleteConfirmDialog: false,
      routerConfirmDialog: false,
      actioned: false
    };
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
      if (v.length > 0 && v.length <= 1000) {
        this.contentInvalid = "";
      } else {
        this.contentInvalid = "md-invalid";
      }
    }
  },
  methods: {
    getIconByType() {
      let match: StringMatch = {
        info: "mdi-information-outline",
        warning: "mdi-alert-outline",
        solved: "mdi-check"
      };
      return match[this.type];
    },
    isEdit() {
      return this.$route.name === "admin-edit-event";
    },
    validate(title: string, content: string, type: string) {
      return (
        title.length > 0 &&
        title.length < 40 &&
        content.length > 0 && content.length < 1000 &&
        ["info", "warning", "solved"].includes(type)
      );
    },
    submit() {
      if (this.disableSubmit) {
        return false;
      }
      // Do not let the empty data in, or the frontend array building process will blow up.
      if (!this.validate(this.title, this.content, this.type)) {
        this.snackbarMessage = "发送失败，请检查您填写的内容。";
        this.snackbar = true;
        return false;
      }
      this.$server.post(
        "/api/logue",
        {
          method: this.isEdit() ? "alter" : "submit",
          title: this.title,
          contents: this.content,
          type: this.type,
          id: this.id
        },
        r => {
          if (r.data) {
            this.disableSubmit = true;
            this.snackbarMessage = "成功发布新的事件，即将为您跳转";
            this.snackbar = true;
            this.actioned = true;
            setTimeout(() => {
              this.$router.push({
                name: "admin-panel"
              });
            }, 1500);
          } else {
            this.snackbarMessage = "发送失败，请检查控制台";
            this.snackbar = true;
          }
        }
      );
    },
    deleteEvent() {
      this.$server.post(
        "/api/logue",
        {
          method: "delete",
          id: this.id
        },
        r => {
          if (r.data) {
            this.snackbarMessage = "成功删除此事件，即将返回首页";
            this.snackbar = true;
            this.actioned = true;
            setTimeout(() => {
              this.$router.push({
                name: "home"
              });
            }, 1500);
          } else {
            this.snackbarMessage = "由于发生了内部错误，删除失败";
            this.snackbar = true;
          }
        }
      );
    },
    next() {}
  },
  mounted() {
    if (this.isEdit()) {
      this.id = Number(this.$route.params.id);
      if (this.id > 0 && Number.isInteger(this.id) && this.id !== NaN) {
        this.$server.get(
          "/api/logue?method=id&markdown=false&id=" + this.id,
          r => {
            let data = r.data;
            if (r.data) {
              this.title = data.title;
              this.content = data.contents;
              this.type = data.type;
            } else {
              this.invalidID = true;
            }
          }
        );
      } else {
        this.invalidID = true;
      }
    }
    window.onbeforeunload = e => {
      if (this.$route.name === "admin-new-event" && (this.title.length > 0 || this.content.length > 0)) {
        e = e || window.event;
        if (e) {
          e.returnValue = "是否确实要离开此页面？您的修改将不会被保存。";
        }
        return "是否确实要离开此页面？您的修改将不会被保存。";
      } else {
        window.onbeforeunload = null;
      }
    };
  },
  beforeRouteLeave(to, from, next) {
    if ((this.title.length > 0 || this.content.length > 0) && !this.actioned) {
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
.new-event-form {
  .textarea {
    position: relative;
    height: 50%;

    @media screen and (max-width: 1024px) {
      height: 60%;
    }

    textarea {
      position: relative;
      min-height: 100% !important;
      resize: none !important;
    }
  }

  .submit-btn {
    margin-top: 56px !important;
    display: block;
    margin: auto;
  }
}

.functions {
  position: absolute;
  top: 32px;
  right: 0;
  display: flex;
  align-items: center;
}

.hero {
  @media screen and (max-width: 1024px) {
    h1 {
      font-size: 38px;
    }
    p {
      font-size: 18px;
    }
  }
}
</style>