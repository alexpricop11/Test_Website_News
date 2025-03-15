<template>
  <form @submit.prevent="loginUser" class="space-y-4">
    <div class="form-group">
      <input type="text" v-model="form.username" placeholder="Numele" required class="input-field">
      <div v-if="errors.username" class="error-message">{{ errors.username }}</div>
    </div>

    <div class="form-group">
      <input :type="showPassword ? 'text' : 'password'" v-model="form.password" placeholder="Parola" required
             class="input-field">
      <button type="button" class="password-toggle" @click="showPassword = !showPassword">
        <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
      </button>
      <div v-if="errors.password" class="error-message">{{ errors.password }}</div>
    </div>

    <button type="submit" class="submit-button">Login</button>

    <div v-if="generalError" class="error-message general">{{ generalError }}</div>
  </form>
</template>

<script>
import {ref} from 'vue';
import router from '@/router/routing.js';
import apiClient from '@/api.js';

export default {
  name: 'LoginForm',
  setup() {
    const showPassword = ref(false);
    const form = ref({
      username: '',
      password: ''
    });
    const errors = ref({});
    const generalError = ref('');

    const loginUser = async () => {
      errors.value = {};
      generalError.value = '';
      try {
        const response = await apiClient.post('/login/', form.value);
        localStorage.setItem('token', response.data.token);
        await router.push('/');
      } catch (error) {
        if (error.response && error.response.data) {
          if (error.response.data.detail) {
            generalError.value = error.response.data.detail;
          } else {
            errors.value = error.response.data;
          }
        } else if (error.message) {
          generalError.value = error.message;
        } else {
          generalError.value = 'A apărut o eroare necunoscută.';
        }
      }
    };

    return {
      showPassword,
      form,
      errors,
      generalError,
      loginUser
    };
  }
};
</script>

<style scoped>
form {
  max-width: 300px;
  margin: 20px auto;
  padding: 20px;
  border-radius: 6px;
  color: #ffffff;
}

.form-group {
  position: relative;
  margin-bottom: 15px;
}

.input-field {
  width: 100%;
  padding: 10px;
  border: 1px solid #4a5568;
  border-radius: 4px;
  font-size: 14px;
  background-color: #1a202c;
  color: #ffffff;
}

.input-field:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 5px rgba(74, 144, 226, 0.3);
}

.input-field::placeholder {
  color: #a0aec0;
  opacity: 1;
}

.password-toggle {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #a0aec0;
  font-size: 16px;
}

.password-toggle:hover {
  color: #ffffff;
}

.error-message {
  color: #e53e3e;
  font-size: 12px;
  margin-top: 5px;
}

.error-message.general {
  margin-top: 10px;
}

.submit-button {
  width: 100%;
  padding: 12px;
  background-color: #48bb78;
  color: #ffffff;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #38a169;
}
</style>