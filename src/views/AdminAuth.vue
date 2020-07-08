<template>
    <div class="admin-auth">
        <div class="auth-container">
            <div class="auth-box">
                <Logo class="auth-img" />
                <md-field>
                    <md-icon class="mdi mdi-account-circle" />
                    <label>用户名</label>
                    <md-input v-model="username" type="text" @keyup.enter="submit()" />
                    <span class="md-helper-text">您的用户名。</span>
                </md-field>
                <md-field>
                    <md-icon class="mdi mdi-textbox-password" />
                    <label>密码</label>
                    <md-input v-model="password" type="password" @keyup.enter="submit()" />
                    <span class="md-helper-text">您的密码。</span>
                </md-field>
                <md-button @click="submit()" class="login-btn md-primary md-raised">
                    登录
                </md-button>
                <md-snackbar
                    md-position="center"
                    :md-duration="1500"
                    :md-active.sync="snackbar"
                    md-persistent
                >{{ snackbarMessage }}</md-snackbar>
                <md-dialog :md-active="loginLoading">
                    <md-dialog-title>请稍候...</md-dialog-title>
                </md-dialog>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
// @ts-ignore
import MdField from "vue-material/dist/components/MdField";
import Logo from "../components/Logo.vue";
// @ts-ignore
import MdProgress from "vue-material/dist/components/MdProgress";

Vue.use(MdField)
    .use(MdProgress);

export default Vue.extend({
    data() {
        return {
            username: "",
            password: "",
            snackbar: false,
            snackbarMessage: "",
            loginLoading: false
        };
    },
    components: {
        Logo
    },
    created() {
        this.$server.post(
            "/api/auth",
            {
                method: "auth"
            },
            r => {
                if (r.data) {
                    this.$router.push({
                        name: "admin-panel"
                    });
                }
            }
        );
    },
    methods: {
        submit() {
            this.loginLoading = true;
            this.$server.post(
                "/api/auth",
                {
                    method: "login",
                    username: this.username,
                    password: this.password
                },
                r => {
                    this.loginLoading = false;
                    if (r.data) {
                        this.snackbarMessage = "登录成功，正在为您跳转";
                        this.snackbar = true;
                        setTimeout(() => {
                            this.$router.push({
                                name: "admin-panel"
                            });
                        }, 1500);
                    } else {
                        this.snackbarMessage = "登录失败，请检查您填写的信息";
                        this.snackbar = true;
                    }
                }
            );
        }
    }
});
</script>

<style lang="less" scoped>
.admin-auth,
.auth-container {
    align-items: center;
    min-height: 100%;
}

.auth-container {
    display: flex;

    .auth-box {
        min-width: 310px;

        &,
        .login-btn {
            display: block;
            margin: auto;
        }

        .login-btn {
            margin-top: 56px;
        }

        .auth-img {
            width: 200px;
            display: block;
            margin: auto;
        }
    }
}
</style>