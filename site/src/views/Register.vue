<template>
    <div class="container mt-5">
        <h1>Register</h1>

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
                <label for="registerConfirmPassword" class="form-label">Confirm password</label>
                <input v-model="confirmPassword" type="password" class="form-control" id="registerConfirmPassword">
            </div>
            <button type="button" @click.stop.prevent="register" class="btn btn-primary" :disabled="formInvalid()" >Register</button>
        </form>
    </div>
</template>
<script setup>
    import { ref } from "vue";
    import { getAuth, createUserWithEmailAndPassword } from "firebase/auth";
    import { useRouter} from "vue-router";
    import utils from "../utils.js";
    import { useToastStore } from "../stores/messages";

    const toastStore = useToastStore();
    const email = ref("");
    const password = ref("");
    const confirmPassword = ref("");
    const router = useRouter();

    const register = () => {
        createUserWithEmailAndPassword(getAuth(), email.value, password.value)
        .then((data) => {
            router.push("/");
        })
        .catch((error) => {
            toastStore.error(error.message);
        })
    }

    const formInvalid = () => {
        if (!(email.value.length != 0 && password.value.length >= 8)) return true;
        if (!utils.emailValid(email.value)) return true;
        if (password.value != confirmPassword.value) return true;

        return false;
    }
    
    
</script>