<template>
    <div class="container mt-5">
    <div class="row">
      <div class="col-md-12">
          <h1>Sign In</h1>
          <p><input type="text" v-model="email" placeholder="Email" /></p>
          <p><input type="password" v-model="password" placeholder="Password" /></p>
          <p v-if="errorMessage">{{errorMessage}}</p>
          <p><button @click="register">Submit</button></p>
          <p><button @click="signInWithGoogle">Sign In with Google</button></p>
      </div>
    </div>
  </div>
</template>
<script setup>
    import { ref } from "vue";
    import { getAuth, signInWithEmailAndPassword , GoogleAuthProvider, signInWithPopup} from "firebase/auth";
    import { useRouter} from "vue-router";
    const email = ref("");
    const password = ref("");
    const errorMessage = ref();
    const router = useRouter();
    const register = () => {
        const auth = getAuth();
        signInWithEmailAndPassword(auth, email.value, password.value)
        .then((data) => {
            console.log("successfully signed in");
            console.log(auth.currentUser);
            router.push("/portfolio");
        })
        .catch((error) => {
            console.log(error.code);
            switch(error.code) {
                case "auth/invalid-email":
                    errorMessage.value = "Invalid Email";
                    break;
                default:
                    errorMessage.value = "Invalid Email or Password";
                    break;
            }
        })
    }
    const signInWithGoogle = () => {
        const provide = new GoogleAuthProvider();
        signInWithPopup(getAuth(), provide)
            .then((result) => {
                console.log(result.user);
                router.push("/portfolio");
            })
            .catch((error) => {

            });
    }
</script>