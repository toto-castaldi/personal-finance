import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
    history: createWebHistory(
        import.meta.env.BASE_URL),
    routes: [
      { path: "/", component: () => import("../views/Home.vue")},
      { path: "/register", component: () => import("../views/Register.vue")},
      { path: "/sign-in", component: () => import("../views/SignIn.vue")},
      { path: "/portfolio", component: () => import("../views/Portfolio.vue")},
   ],
});

export default router;