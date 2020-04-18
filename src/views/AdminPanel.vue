<template>
    <div v-if="auth" class="admin-panel">
        <div class="hero">
            <h1>控制中心</h1>
            <p>选择您要进行的操作</p>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
    data() {
        return {
            auth: false
        }
    },
    created() {
        this.$server.post("/api/auth", {
            method: "auth"
        }, r => {
            if (!r.data) {
                this.$router.push({
                    name: "admin-auth"
                })
            } else {
                this.auth = true;
            }
        })
    }
})
</script>