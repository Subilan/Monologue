export function isPC(): boolean {  
    var userAgentInfo = navigator.userAgent;
    var Agents = new Array("Android", "iPhone", "SymbianOS", "Windows Phone", "iPad", "iPod");  
    var flag = true;  
    for (var v = 0; v < Agents.length; v++) {  
        if (userAgentInfo.indexOf(Agents[v]) > 0) { flag = false; break; }  
    }  
    return flag;
 }

 // do not use the function in return or if statements because there is something async which is impossible to return a value in a sync way.
 export function copy(text: string, callback: Function | undefined = undefined): boolean {
     if (!navigator.clipboard) {
         let a = document.createElement("textarea");
         a.value = text;
         a.style.top = "0";
         a.style.left = "0";
         a.style.position = "fixed";

         document.body.appendChild(a);
         a.focus();
         a.select();
         try {
             return document.execCommand("copy");
         } catch (e) {
             return false;
         }
         document.body.removeChild(a);
     } else {
         navigator.clipboard.writeText(text).then(r => {
             if (callback) {
                callback();
             }
         }, err => {
             console.error(err);
         });
         return true;
     }
 }