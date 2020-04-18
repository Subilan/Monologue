import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
	{
		path: "/",
		name: "home",
		component: () => import("@/views/Home.vue")
	},
	{
		path: "/admin",
		name: "admin",
		component: () => import("@/views/Admin.vue"),
		children: [
			{
				path: "new",
				name: "admin-new",
				component: () => import("@/views/AdminNew.vue")
			}
		]
	}
];

const router = new VueRouter({
	mode: "history",
	scrollBehavior (to, from, spos) {
		if (to.hash) {
			return {
				selector: to.hash
			}
		} else {
			return {
				x: 0,
				y: 0,
			}
		}
	},
	base: process.env.BASE_URL,
	routes
});

export default router;
