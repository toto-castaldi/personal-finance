<template>
  <div class="container mt-3 overflow-hidden">
    <div class="row gx-5">
      <div class="p-3 col">
          <Cryptos />
      </div>
    </div>
    <div class="row gx-5">
      <div class="p-3 col">
          <CryptoMovements />
      </div>
    </div>
  </div>
</template>

<script>

import CryptoMovements from "../components/CryptoMovements.vue";
import Cryptos from "../components/Cryptos.vue";

export default {
    data() {
        return {
        }
    },
    components: {
      CryptoMovements, Cryptos
    },
    methods : {
    }
}


</script>

