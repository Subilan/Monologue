import qs from 'qs';
import axios from 'axios';

class Server {
    public static post(url: string, data: object, callback: Function) {
        axios.post(url, qs.stringify(data)).then(r => {
            callback(r);
        }).catch(r => {
            console.error(r);
        })
    }
}

export default Server;