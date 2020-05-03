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
				path: "panel",
				name: "admin-panel",
				component: () => import("@/views/AdminPanel.vue")
			},
			{
				path: "auth",
				name: "admin-auth",
				component: () => import("@/views/AdminAuth.vue")
			},
		]
	},
	{
		path: "/admin/editor",
		name: "admin-editor",
		component: () => import("@/views/AdminEditor.vue"),
		children: [
			{
				path: "event",
				name: "admin-new-event",
				component: () => import("@/views/AdminNewEvent.vue")
			},
			{
				path: "event/:id?",
				name: "admin-edit-event",
				component: () => import("@/views/AdminNewEvent.vue")
			},
			{
				path: "agreement",
				name: "admin-new-agreement",
				component: () => import("@/views/AdminNewAgreement.vue")
			},
			{
				path: "agreement/:id?",
				name: "admin-edit-agreement",
				component: () => import("@/views/AdminNewAgreement.vue")
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
