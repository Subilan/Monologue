<template>
  <div class="admin-new-event admin-container">
    <div class="hero">
      <h1>添加新事件</h1>
      <p>在时间线上添加新的事件以供外部参考。</p>
    </div>
    <div class="new-event-form">
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

Vue.use(MdField)
  .use(MdIcon)
  .use(MdButton)
  .use(MdMenu)
  .use(MdList)
  .use(MdSnackbar);

export default Vue.extend({
  data() {
    return {
      title: "",
      content: "",
      type: "info",
      titleInvalid: "",
      contentInvalid: "",
      snackbar: false,
      snackbarMessage: "",
      disableSubmit: false
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
    submit() {
      if (this.disableSubmit) {
        return false;
      }
      this.$server.post(
        "/api/logue",
        {
          title: this.title,
          contents: this.content,
          type: this.type
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
  }
});
</script>

<style lang="less" scoped>
.new-event-form {
  height: 100%;
  position: relative;

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