<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-desk navbar-dark bg-dark">
      <div class="container">
        <router-link class="navbar-brand" to="/">Personal Finance</router-link>
        <button
          class="navbar-toggler navbar-light white"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link active" to="/portfolio">Portfolio</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link active" to="/register">Register</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link active" to="/sign-in">Sign In</router-link>
            </li>
            <li class="nav-item">
              <button @click="handleSignOut" v-if="isLoggedIn" >Sign Out</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>

  <main>
    <router-view />

    <ToastStack />
  </main>
</template>

<script setup>
  import ToastStack from "./components/ToastStack.vue";
  import { onMounted, ref } from "vue";
  import { getAuth, onAuthStateChanged, signOut } from "firebase/auth";
  import { useRouter} from "vue-router";
  const isLoggedIn = ref(false);
  const router = useRouter();
  let auth;
  onMounted(() => {
    auth = getAuth();
    onAuthStateChanged(auth, (user) => {
      if (user) {
        isLoggedIn.value = true;
      } else {
        isLoggedIn.value = false;
      }
    });
  });

  const handleSignOut = () => {
    signOut(auth).then(() => {
      router.push("/");
    });
  }
</script>