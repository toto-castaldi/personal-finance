<template>
    <div class="container mt-5">
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
            <button type="submit" @click="register" class="btn btn-primary">Register</button>
        </form>
    </div>
</template>
<script setup>
    import { ref } from "vue";
    import { getAuth, createUserWithEmailAndPassword } from "firebase/auth";
    import { useRouter} from "vue-router";
    const email = ref("");
    const password = ref("");
    const router = useRouter();
    const register = () => {
        createUserWithEmailAndPassword(getAuth(), email.value, password.value)
        .then((data) => {
            router.push("/portfolio");
        })
        .catch((error) => {
            console.log(error.code);
            alert(error.message);
        })
    }
    
</script>