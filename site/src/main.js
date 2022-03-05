import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

const resp = await fetch("/config.json");
window.config = await resp.json();

const app = createApp(App);

app.use(router);

app.mount("#app");