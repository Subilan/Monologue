interface Dictionary<T> {
	[props: string]: T
}

interface MatchObject {
	[props: string]: Dictionary<string>
}

interface LogueArrayItem {
	date: string;
	logue: Array<Logue>;
}

interface Logue {
	id: number;
	title: string;
	type: string;
	contents: string;
	time: string;
}

interface LogueOrigin extends Logue {
	date: string;
}

interface EditorResult {
	content: string;
	title: string;
}

interface ServerController {
    post(url: string, data: object, callback: Function): void
    get(url: string, callback: Function): void
}