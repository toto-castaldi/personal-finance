import "bootstrap/dist/css/bootstrap.min.css";
import "./assets/global.css";
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { initializeApp } from "firebase/app";
import { createPinia } from "pinia";

const firebaseConfig = {
    apiKey: "AIzaSyCfzN6Xogvmd6AasFEDSEUMGgpgG3RNir0",
    authDomain: "personal-finance-2eb2f.firebaseapp.com",
    projectId: "personal-finance-2eb2f",
    storageBucket: "personal-finance-2eb2f.appspot.com",
    messagingSenderId: "327454650091",
    appId: "1:327454650091:web:7cfc5ca31f8a54780958ae",
    measurementId: "G-44KYTWMYKP"
};

initializeApp(firebaseConfig);
const app = createApp(App);

app.use(createPinia());
app.use(router);
app.mount("#app");

import "bootstrap/dist/js/bootstrap.js";