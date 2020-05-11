/**
 * 根据 UA 判断当前所处设备环境
 * 
 * @return boolean
 */
export function isPC(): boolean {  
    var userAgentInfo = navigator.userAgent;
    var Agents = new Array("Android", "iPhone", "SymbianOS", "Windows Phone", "iPad", "iPod");  
    var flag = true;  
    for (var v = 0; v < Agents.length; v++) {  
        if (userAgentInfo.indexOf(Agents[v]) > 0) { flag = false; break; }  
    }  
    return flag;
 }

/**
 * 复制一段文本到剪贴板
 * 
 * @param {string} text 要复制的文字
 * @param {Function | undefined} callback 处理完毕的回调
 */
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
             document.execCommand("copy");
         } catch (e) {
             return false;
         }
         document.body.removeChild(a);
         return true;
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

 /**
  * 判断一个值是否为合法的日期字符串
  * 
  * @param {any} target 要判断的目标，理论上应当是 string | number
  */
 export function isDate(target: any): boolean {
    let d = new Date(target);
    if (Object.prototype.toString.call(d) === "[object Date]") {
        if (isNaN(d.getTime())) {
            return false;
        } else {
            return true;
        }
    } else {
        return false;
    }
 }

 /**
  * 判断一个字符串是否为数字
  * 
  * @param {string} str 要判断的字符串
  */
 export function isNumericString(str: string): boolean {
     return /^[1-9]\d*$/.test(str);
 }

 /**
  * 生成器函数。创建一个对象的遍历器，使用此遍历器可以在 for ... of 循环中同时得到 Key 和 Value
  * 
  * @param {object} object
  * 
  * @example
  * 
  * 下面是一个使用例子
  * 
  * for (let [k, v] of createIterator(obj)) {
  *     console.log(obj[k] === v);
  *     // => true 
  * }
  */
 export function* createIterator(object: object): Generator<any[], void, unknown> {
     let k = Object.keys(object);
     for (let i = 0; i < k.length; i++) {
         let _k = k[i];
         yield [_k, object[_k]];
     }
 }

 /**
  * 判断是否为桌面视图。如果同时符合 UA 判断和窗口宽度判断，则可以被认定为桌面视图。
  * 
  * 需要注意的是，如果只是桌面平台（即通过了 UA 判断），但是窗口宽度并不足够，仍然会使用移动视图。
  * 
  * @return boolean
  */
 export function isPCView(): boolean {
     return isPC() && window.innerWidth > 1024;
 }

 /**
  * 使用 nzh 将阿拉伯数字转换为简体中文小写
  * 
  * @param number 要转换的数字
  */
export function translateNumber(number: number): string {
    const Nzh = require("nzh");
    const cn = Nzh.cn;
    return cn.encodeS(number);
}

/**
 * 判断一个数字字符串是否在某一范围内（包含两端），仅适用于整数。
 * 
 * @param str 要判断的字符串
 * @param from 起始范围
 * @param to 结束范围
 */
export function isNumericStringBetween(str: string, from: number, to: number): boolean {
    if (isNumericString(str)) {
        let number = Number(str);
        if (Number.isInteger(number)) {
            return number >= from && number <= to;
        }
    }
    return false;
}

/**
 * （不严格）根据字符串内容转换为布尔值
 * 
 * @param str 要转换的字符串
 */
export function stringToBoolean(str: string): boolean {
    return str === "1" || str.toLowerCase() === "true";
}

/**
 * 批量向数组填入同一个值，此值的类型必须符合原数组
 * 
 * @param array 要操作的数组
 * @param value 要填入的值
 * @param length 要填入的值所占长度
 */
export function fillArray<T>(array: Array<T>, value: T, length: number): Array<T> {
    if (length <= 0) {
        return [];
    }
    array.length = length;
    array.fill(value);
    return array;
}