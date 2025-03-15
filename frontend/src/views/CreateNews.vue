<template>
  <form @submit.prevent="createNews" class="space-y-4">
    <div class="form-group">
      <input v-model="form.title" type="text" placeholder="Titlu" required class="input-field"/>
      <div v-if="errors.title" class="error-message">{{ errors.title }}</div>
    </div>

    <div class="form-group">
      <textarea v-model="form.content" placeholder="Conținut" required class="input-field" rows="4"></textarea>
      <div v-if="errors.content" class="error-message">{{ errors.content }}</div>
    </div>

    <div class="form-group">
      <input type="file" @change="onImageChange" accept="image/*" class="input-field"/>
      <div v-if="errors.image" class="error-message">{{ errors.image }}</div>
    </div>

    <div class="form-group">
      <label>
        <input type="checkbox" v-model="form.is_published"/> Publicat
      </label>
    </div>

    <button type="submit" class="submit-button" :disabled="isLoading">
      {{ isLoading ? 'Se creează...' : 'Creează știrea' }}
    </button>
    <div v-if="generalError" class="error-message general">{{ generalError }}</div>
  </form>
</template>

<script setup>
import {ref} from 'vue';
import apiClient from '@/api.js';
import router from '@/router/routing.js';
import {jwtDecode} from 'jwt-decode';

const form = ref({
  title: '',
  content: '',
  image: null,
  is_published: false,
});
const errors = ref({});
const generalError = ref('');
const isLoading = ref(false);

const onImageChange = (event) => {
  form.value.image = event.target.files[0];
};

const createNews = async () => {
  errors.value = {};
  generalError.value = '';
  isLoading.value = true;

  const token = localStorage.getItem('token');
  if (!token) {
    generalError.value = 'Nu ești autentificat. Te rugăm să te loghezi.';
    isLoading.value = false;
    return;
  }

  let userId;
  try {
    const decodedToken = jwtDecode(token);
    userId = decodedToken.user_id;
  } catch (err) {
    generalError.value = 'Token invalid. Te rugăm să te loghezi din nou.';
    isLoading.value = false;
    return;
  }

  const formData = new FormData();
  formData.append('title', form.value.title);
  formData.append('content', form.value.content);
  formData.append('author', userId);
  formData.append('author_id', userId);
  if (form.value.image) formData.append('image', form.value.image);
  formData.append('is_published', form.value.is_published.toString());

  try {
    await apiClient.post('/news/', formData, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'multipart/form-data',
      },
    });
    await router.push('/');
  } catch (error) {
    if (error.response?.data) {
      const data = error.response.data;
      if (data.error) {
        generalError.value = data.error;
      } else {
        Object.keys(data).forEach((key) => {
          errors.value[key] = Array.isArray(data[key]) ? data[key][0] : data[key];
        });
      }
    } else {
      generalError.value = 'A apărut o eroare la crearea știrii.';
    }
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
form {
  max-width: 500px;
  margin: 100px auto;
  padding: 50px;
  border-radius: 5px;
  background-color: #1a202c;
  color: #e2e8f0;
}

.form-group {
  margin-bottom: 15px;
}

.input-field {
  width: 100%;
  padding: 10px;
  border: 1px solid #4a5568;
  border-radius: 4px;
  font-size: 14px;
  background-color: #2d3748;
  color: #e2e8f0;
}

.input-field:focus {
  outline: none;
  border-color: #4a90e2;
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
  cursor: pointer;
}

.submit-button:hover:not(:disabled) {
  background-color: #38a169;
}

.submit-button:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}
</style>