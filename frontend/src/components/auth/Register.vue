<template>
  <form @submit.prevent="registerUser" class="space-y-4">
    <div class="form-group">
      <input type="text" v-model="form.username" placeholder="Numele" required
             class="input-field">
    </div>

    <div class="form-group">
      <input :type="showPassword ? 'text' : 'password'" v-model="form.password" placeholder="Parola" required
             class="input-field">
      <button type="button" class="password-toggle"
              @click="showPassword = !showPassword">
        <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
      </button>
    </div>

    <div class="form-group">
      <input type="email" v-model="form.email" placeholder="Email"
             class="input-field">
    </div>

    <button type="submit"
            class="submit-button">
      Înregistrează-te
    </button>
  </form>
</template>

<script setup>
import {nextTick, ref} from 'vue'
import apiClient from "@/api.js";
import router from "@/router/routing.js";

const showPassword = ref(false)
const form = ref({
  username: null,
  password: null,
  email: null,
})
const errors = ref({});

const registerUser = async () => {
  errors.value = {};
  if (!form.value.email) {
    form.value.email = null;
  }
  try {
    const response = await apiClient.post('/register/', form.value);
    localStorage.setItem('token', response.data.token);
    await nextTick(() => {
      router.push('/');
    });
  } catch (error) {
    if (error.response && error.response.data) {
      errors.value = error.response.data.detail;
    } else {
      console.error('Registration error:', error);
    }
  }
};
</script>

<style scoped>
form {
  max-width: 300px;
  margin: 20px auto;
  padding: 20px;
  border-radius: 5px;
}

.form-group {
  position: relative;
  margin-bottom: 15px;
}

.input-field {
  width: 100%;
  padding: 10px;
  border: 1px solid #ffffff;
  border-radius: 4px;
  font-size: 14px;
  background-color: #07091b;
  color: #ffffff;
}

.input-field:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.3);
}

.password-toggle {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #666;
  font-size: 16px;
}

.password-toggle:hover {
  color: #007bff;
}

.submit-button {
  width: 100%;
  padding: 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #45a049;
}

.input-field::placeholder {
  color: #ffffff;
  opacity: 1;
}
</style>
