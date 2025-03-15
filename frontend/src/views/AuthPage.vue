<template>
  <div class="container">
    <div class="button-group">
      <button
          class="button half left"
          :class="{ active: isRegisterActive }"
          @click="isRegisterActive = true">
        Înregistrare
      </button>
      <button
          class="button half right"
          :class="{ active: !isRegisterActive }"
          @click="isRegisterActive = false">
        Login
      </button>
    </div>

    <Register v-if="isRegisterActive"/>
    <Login v-else/>
  </div>
</template>

<script setup>
import {ref} from 'vue';
import Login from '@/components/Auth/Login.vue';
import Register from '@/components/Auth/Register.vue';

const isRegisterActive = ref(true);
</script>

<style scoped>
.container {
  max-width: 480px;
  margin: 20px auto;
  padding: 20px;
  background-color: #1a202c;
  border-radius: 8px;
  color: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.button-group {
  display: flex;
  margin-bottom: 20px;
}

.button {
  flex: 1;
  padding: 12px;
  font-size: 16px;
  font-weight: bold;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.left {
  border-top-left-radius: 6px;
  border-bottom-left-radius: 6px;
}

.right {
  border-top-right-radius: 6px;
  border-bottom-right-radius: 6px;
}

.button.active {
  background-color: #4CAF50;
  color: #ffffff;
}

.button:not(.active) {
  background-color: #2d3748;
  color: #ffffff;
}

.button:not(.active):hover {
  background-color: #4a5568;
}
</style>
