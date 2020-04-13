import qs from 'qs';
import axios from 'axios';

class Server {
    public post(data: object, callback: Function) {
        axios.post("/api/data.php", qs.stringify(data)).then(r => {
            callback(r);
        }).catch(r => {
            console.error(r);
        })
    }
}

export default Server;