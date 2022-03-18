import { createRouter, createWebHistory } from "vue-router";
import { getAuth, onAuthStateChanged } from "firebase/auth";
import { useToastStore } from "../stores/messages";

const router = createRouter({
    history: createWebHistory(
        import.meta.env.BASE_URL),
    routes: [{
            path: "/",
            component: () =>
                import ("../views/Home.vue")
        },
        {
            path: "/register",
            component: () =>
                import ("../views/Register.vue"),
            meta: { requiresAuth: false }
        },
        {
            path: "/sign-in",
            component: () =>
                import ("../views/SignIn.vue"),
            meta: { requiresAuth: false }
        },
        {
            path: "/portfolio",
            component: () =>
                import ("../views/Portfolio.vue"),
            meta: { requiresAuth: true }
        },
    ],
});

const getCurrentUser = () => {
    return new Promise((resolve, reject) => {
        const removeListener = onAuthStateChanged(getAuth(), (user) => {
            removeListener();
            resolve(user);
        }, reject);
    });
}

router.beforeEach(async(to, from, next) => {
    const store = useToastStore();
    if ("requiresAuth" in to.meta) {
        const user = await getCurrentUser();
        const logged = user != null;
        if (to.meta.requiresAuth && logged) {
            next();
        } else if (!to.meta.requiresAuth && !logged) {
            next();
        } else if (to.meta.requiresAuth && !logged) {
            store.error("you can't access");
            next("/sign-in");
        } else if (!to.meta.requiresAuth && logged) {
            store.error("you can't access");
            next("/");
        }
    } else {
        next();
    }

});

export default router;