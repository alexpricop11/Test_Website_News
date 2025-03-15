<template>
  <div>
    <p v-if="userName">Bun venit, {{ userName }}!</p>
  </div>
</template>

<script setup>
import {ref, onMounted} from "vue";
import {jwtDecode} from "jwt-decode";

const userName = ref("");

const getUserNameFromToken = () => {
  const token = localStorage.getItem("token");
  if (token) {
    try {
      const decoded = jwtDecode(token);
      userName.value = decoded.username;
    } catch (error) {
      console.error("Eroare la decodarea token-ului:", error);
    }
  }
};


onMounted(getUserNameFromToken);
</script>

<style scoped>

</style>
