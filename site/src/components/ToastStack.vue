<template>
  <div
    class="toast-container position-fixed bottom-0 end-0 p-3"
    style="z-index: 11"
  >
    <div
      class="bg-danger text-white fade toast show"
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
      v-for="error in store.errorList"
    >
      <div class="toast-header bg-danger text-white">
        <strong class="me-auto">Error</strong>
        <small></small>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="toast"
          aria-label="Close"
        ></button>
      </div>
      <div class="toast-body ">{{ error }}</div>
    </div>
  </div>
</template>

<script>
import { useToastStore } from "../stores/messages";

export default {
  setup() {
    const store = useToastStore();
    return {
      store
    };
  },
};
</script>