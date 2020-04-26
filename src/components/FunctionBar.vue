<template>
    <div>
        <div v-if="isPC() || singleOnMobile" class="functions">
            <slot></slot>
        </div>

        <md-menu
            v-if="!isPC() && !singleOnMobile"
            md-direction="bottom-start"
            class="mobile-menu-btn"
        >
            <md-button md-menu-trigger class="md-raised md-icon-button">
                <md-icon class="mdi mdi-plus-circle" />
            </md-button>
            <md-menu-content class="mobile-menu">
                <slot></slot>
            </md-menu-content>
        </md-menu>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
// @ts-ignore
import MdMenu from "vue-material/dist/components/MdMenu";
// @ts-ignore
import MdList from "vue-material/dist/components/MdList";
// @ts-ignore
import MdIcon from "vue-material/dist/components/MdIcon";
// @ts-ignore
import MdButton from "vue-material/dist/components/MdButton";
import { isPC } from "@/functions";

Vue.use(MdMenu)
    .use(MdList)
    .use(MdIcon)
    .use(MdButton);

export default Vue.extend({
    data() {
        return {
            singleOnMobile: false
        };
    },
    methods: {
        isPC
    },
    mounted() {
        if (
            //@ts-ignore
            (this.$slots.default.length === 2 &&
                //@ts-ignore
                this.$slots.default[0].tag === undefined) ||
            //@ts-ignore
            this.$slots.default.length === 1
        ) {
            this.singleOnMobile = true;
        }
    }
});
</script>

<style lang="less" scoped>
.functions {
    @media screen and (max-width: 1024px) {
        top: -16px;
    }

    @media screen and (min-width: 1024px) {
        top: 32px;
    }

    position: absolute;
    right: 0;
    display: flex;
    align-items: center;

    * {
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

.mobile-menu-btn {
    position: absolute;
    top: -16px;
    right: 0;
}

.mobile-menu {
    display: flex;
    align-items: center;
}
</style>