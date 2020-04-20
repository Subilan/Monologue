interface StringMatch {
	[props: string]: string;
}

interface MatchObject {
	[props: string]: StringMatch;
}

interface LogueArrayItem {
	date: string;
	time: string;
	logue: Array<Logue>;
}

interface Logue {
	title: string;
	type: string;
	contents: string;
}

interface LogueOrigin extends Logue {
	date: string;
	id: number;
}
