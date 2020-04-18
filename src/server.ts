import axios from 'axios';

declare module "vue/types/vue" {
	interface Vue {
		$server: ServerController;
	}
}

interface ServerController {
	post(url: string, data: object, callback: Function): void
}

const Server: ServerController = class {
    public static post(url: string, data: object, callback: Function) {
        axios.post(url, JSON.stringify(data)).then(r => {
            callback(r);
        }).catch(r => {
            console.error(r);
        })
    }
}

export default Server;