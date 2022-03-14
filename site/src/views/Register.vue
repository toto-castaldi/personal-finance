<template>
    <div class="container mt-5">
    <div class="row">
      <div class="col-md-12">
          <h1>Register</h1>
          <p><input type="text" v-model="email" placeholder="Email" /></p>
          <p><input type="password" v-model="password" placeholder="Password" /></p>
          <p><button @click="register">Submit</button></p>
          <p><button @click="signInWithGoogle">Sign In with Google</button></p>
      </div>
    </div>
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
            console.log("successfully registered");
            router.push("/portfolio");
        })
        .catch((error) => {
            console.log(error.code);
            alert(error.message);
        })
    }
    const signInWithGoogle = () => {

    }
</script>