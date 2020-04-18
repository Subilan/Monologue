<template>
    <div class="admin">
        <router-view/>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
    data() {

    },
    mounted() {
        this.$server.post({
            method: "auth"
        }, r => {
            console.log(r.data);
        })
    }
})
</script>