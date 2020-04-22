<template>
  <div class="admin-event admin-container">
    <md-empty-state v-if="invalidID">
      <span class="md-empty-state-icon mdi mdi-help-circle-outline"/>
      <span class="md-empty-state-label">无效的 ID</span>
      <span class="md-empty-state-description">您输入的 ID 有误或者不存在</span>
      <md-button @click="$router.go(-1)" class="md-primary md-raised">后退</md-button>
    </md-empty-state>
    <div class="full-height" v-if="!isEdit() || !invalidID">
      <div class="hero">
        <h1>{{ isEdit() ? "编辑事件 #" + id : "添加新事件"}}</h1>
        <p>{{ isEdit() ? "修改该事件的内容和相关属性。" : "在时间线上添加新的事件以供外部参考。" }}</p>
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
          :md-duration="3000"
          md-persistent
        >{{ snackbarMessage }}</md-snackbar>
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

Vue.use(MdField)
  .use(MdIcon)
  .use(MdButton)
  .use(MdMenu)
  .use(MdList)
  .use(MdSnackbar)
  .use(MdEmptyState);

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
    submit() {
      if (this.disableSubmit) {
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
            setTimeout(() => {
              this.$router.push({
                name: "admin-panel"
              });
            }, 3000);
          } else {
            this.snackbarMessage = "发送失败，请检查控制台";
            this.snackbar = true;
          }
        }
      );
    }
  },
  mounted() {
    if (this.isEdit()) {
      this.id = Number(this.$route.params.id);
      if (this.id > 0 && Number.isInteger(this.id) && this.id !== NaN) {
        this.$server.get("/api/logue?method=id&markdown=false&id=" + this.id, r => {
          let data = r.data;
          this.title = data.title;
          this.content = data.contents;
          this.type = data.type;
        });
      } else {
        this.invalidID = true;
      }
    }
  }
});
</script>

<style lang="less" scoped>
.new-event-form {
  .textarea {
    position: relative;
    height: 50% !important;

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
</style>