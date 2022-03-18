<template>
    <div class="container mt-5">
        <h1>Sign In</h1>

        <form>
            <div class="mb-3">
                <label for="registerEmail" class="form-label">Email address</label>
                <input type="email" v-model="email" class="form-control" id="registerEmail" aria-describedby="emailHelp">
                <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
            </div>
            <div class="mb-3">
                <label for="registerPassword" class="form-label">Password</label>
                <input v-model="password" type="password" class="form-control" id="registerPassword">
            </div>
            <div class="mb-3">
                <button type="button" @click.stop.prevent="signIn" class="btn btn-primary" :disabled="formInvalid()" >Sing In</button>
            </div>
            <div class="mb-3">
                <button type="button" @click.stop.prevent="signInWithGoogle" class="btn btn-primary" >Sign In with Google</button>
            </div>
        </form>
    </div>
</template>
<script setup>
    import { ref } from "vue";
    import { getAuth, signInWithEmailAndPassword , GoogleAuthProvider, signInWithPopup} from "firebase/auth";
    import { useRouter} from "vue-router";
    import { useToastStore } from "../stores/messages";

    const toastStore = useToastStore();
    const email = ref("");
    const password = ref("");
    const router = useRouter();

    const formInvalid = () => {
        if (!(email.value.length != 0 && password.value.length >= 8)) return true;

        return false;
    }
    const signIn = () => {
        const auth = getAuth();
        signInWithEmailAndPassword(auth, email.value, password.value)
        .then((data) => {
            router.push("/portfolio");
        })
        .catch((error) => {
            switch(error.code) {
                case "auth/invalid-email":
                    toastStore.error("Invalid Email");
                    break;
                default:
                    toastStore.error("Invalid Email or Password");
                    break;
            }
        })
    }
    const signInWithGoogle = () => {
        const provide = new GoogleAuthProvider();
        signInWithPopup(getAuth(), provide)
            .then((result) => {
                router.push("/portfolio");
            })
            .catch((error) => {
                toastStore.error(error);
            });
    }
</script>