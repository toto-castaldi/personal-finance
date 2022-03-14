<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-desk bg-dark">
      <div class="container">
        <router-link class="navbar-brand" to="/">Personal Finance</router-link>
        <button
          class="navbar-toggler"
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
          </ul>
        </div>
      </div>
    </nav>
  </header>

  <main>
    <router-view />
  </main>
</template>