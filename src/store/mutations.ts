import Vue from "vue";

const makeStyles = <T extends string = string>(styles: Record<T, string>): Record<T, string> => {
	return styles;
};

const data = makeStyles({
	CHANGE_EDITOR_COMMITED_STATE: "changeEditorCommitedState"
});

declare module "vue/types/vue" {
	interface Vue {
		$mutations: typeof data;
	}
}

export default data;
