"use strict";
exports.__esModule = true;
var vue_1 = require("vue");
var vue_router_1 = require("vue-router");
vue_1["default"].use(vue_router_1["default"]);
var routes = [
    {
        path: "/",
        name: "home",
        component: function () { return Promise.resolve().then(function () { return require("@/views/Home.vue"); }); }
    },
    {
        path: "/admin",
        name: "admin",
        component: function () { return Promise.resolve().then(function () { return require("@/views/Admin.vue"); }); },
        children: [
            {
                path: "new",
                name: "admin-new",
                component: function () { return Promise.resolve().then(function () { return require("@/views/AdminNew.vue"); }); }
            }
        ]
    }
];
var router = new vue_router_1["default"]({
    mode: "history",
    scrollBehavior: function (to, from, spos) {
        if (to.hash) {
            return {
                selector: to.hash
            };
        }
        else {
            return {
                x: 0,
                y: 0
            };
        }
    },
    base: process.env.BASE_URL,
    routes: routes
});
exports["default"] = router;
