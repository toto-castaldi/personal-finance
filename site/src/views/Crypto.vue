<template>
  <div class="container mt-3 overflow-hidden">
    <div class="row gx-5">
      <div class="p-3 col">
          <CryptoApr />
      </div>
    </div>
    <div class="row gx-5">
      <div class="p-3 col">
          <Cryptos />
      </div>
    </div>
    <div class="row gx-5">
      <div class="p-3 col">
          <PortfolioTrend :levelInfo="newLevel" />
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
import PortfolioTrend from "../components/PortfolioTrend.vue";
import CryptoMovements from "../components/CryptoMovements.vue";
import Cryptos from "../components/Cryptos.vue";
import CryptoApr from "../components/CryptoApr.vue";

export default {
    data() {
        return {
          newLevel : { level : 1, node : "CRYPTO"}
        }
    },
    components: {
      CryptoMovements, Cryptos, CryptoApr, PortfolioTrend
    },
    methods : {
    }
}


</script>

