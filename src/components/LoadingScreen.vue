<template>
    <div class="loading-screen">
        <div class="loading">
            <md-progress-spinner md-mode="indeterminate" />
        </div>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
// @ts-ignore
import MdProgress from "vue-material/dist/components/MdProgress";

Vue.use(MdProgress);

export default Vue.extend({});
</script>