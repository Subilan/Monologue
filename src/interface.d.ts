interface StringMatch {
	[props: string]: string;
}

interface MatchObject {
	[props: string]: StringMatch;
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
