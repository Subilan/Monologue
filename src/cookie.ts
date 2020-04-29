import Cookies from 'js-cookie';

export function setcookie(name: string, value: any, expires: number = Infinity): string | undefined {
    return Cookies.set(name, value, {
        expires
    })
}

export function delcookie(name: string): void {
    Cookies.remove(name);
}

export function getcookie(name: string): any {
    return Cookies.get(name);
}