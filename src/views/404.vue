<template>
    <div class="error-not-found full-height">
        <md-empty-state>
            <span class="md-empty-state-icon mdi mdi-help-circle-outline"/>
            <span class="md-empty-state-label">404</span>
            <span class="md-empty-state-description">找不到该页面</span>
            <md-button @click="$router.go(-1)" class="md-primary md-raised">&laquo; 后退</md-button>
        </md-empty-state>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
// @ts-ignore
import MdButton from 'vue-material/dist/components/MdButton';
// @ts-ignore
import MdEmptyState from 'vue-material/dist/components/MdEmptyState';

Vue.use(MdButton).use(MdEmptyState);

export default Vue.extend({

})
</script>