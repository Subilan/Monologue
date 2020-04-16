"use strict";
exports.__esModule = true;
var vue_1 = require("vue");
var App_vue_1 = require("./App.vue");
require("./registerServiceWorker");
var router_1 = require("./router");
require("@/css/mono.less");
require("@mdi/font/css/materialdesignicons.min.css");
var server_1 = require("@/server");
require("vue-material/dist/vue-material.min.css");
require("./css/default.css");
require("./css/override.less");
vue_1["default"].config.productionTip = false;
vue_1["default"].prototype.$server = server_1["default"];
new vue_1["default"]({
    router: router_1["default"],
    render: function (h) { return h(App_vue_1["default"]); }
}).$mount('#app');
