import axios from 'axios';
import Vue from 'vue';

declare module "vue/types/vue" {
    interface Vue {
        $server: ServerController;
    }
}

const Server: ServerController = class {
    public static post(url: string, data: object, callback: Function) {
        axios.post(url, JSON.stringify(data)).then(r => {
            callback(r);
        }).catch(r => {
            console.error(r);
        })
    }

    public static get(url: string, callback: Function) {
        axios.get(url).then(r => {
            callback(r);
        }).catch(r => {
            console.error(r);
        })
    }
}

export default Server;