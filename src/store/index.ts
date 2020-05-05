import Vue from 'vue';
import Vuex from 'vuex';
import * as mutations from './mutations';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        editorCommited: false  
    },
    mutations: {
        [mutations.CHANGE_EDITOR_COMMITED_STATE] (state, p) {
            state.editorCommited = p.state;
        }
    }
})