<template>
  <h1>Știrile mele</h1>
  <div class="news-list">
    <div v-if="isLoading">Se încarcă...</div>
    <div v-else-if="news.length === 0">Nu ai știri încă.</div>
    <ul v-else>
      <li v-for="item in news" :key="item.id" class="news-item">
        <h2>{{ item.title }}</h2>
        <p>{{ item.content }}</p>
        <img v-if="item.image" :src="item.image" alt="News Image" class="news-image" @error="handleImageError(item)"/>
        <p>Publicat: {{ formatDate(item.published_at) }}</p>
        <p>Status: {{ item.is_published ? 'Publicat' : 'Nepublicat' }}</p>
        <div class="buttons">
          <button @click="openEditModal(item)" class="edit-button">Editează</button>
          <button @click="deleteNews(item.id)" class="delete-button">Șterge</button>
        </div>
      </li>
    </ul>
    <div v-if="error" class="error-message">{{ error }}</div>
  </div>

  <!-- Edit Modal -->
  <div v-if="showEditModal" class="modal-overlay" @click.self="closeEditModal">
    <div class="modal">
      <div class="modal-header">
        <h2>Editează Știrea</h2>
        <button @click="closeEditModal" class="close-icon">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <form @submit.prevent="updateNews" class="edit-form">
        <div class="form-group">
          <label for="title">Titlu</label>
          <input v-model="editForm.title" id="title" type="text" required/>
        </div>
        <div class="form-group">
          <label for="content">Conținut</label>
          <textarea v-model="editForm.content" id="content" rows="5" required></textarea>
        </div>
        <div class="form-group">
          <label for="image">Imagine (lasă necompletat pentru a păstra imaginea existentă)</label>
          <input type="file" id="image" @change="handleImageUpload" accept="image/*"/>
          <img v-if="editForm.imagePreview" :src="editForm.imagePreview" alt="Image Preview" class="image-preview"/>
        </div>
        <div class="form-group">
          <label for="is_published">Publicat</label>
          <input v-model="editForm.is_published" id="is_published" type="checkbox"/>
        </div>
        <button type="submit" :disabled="isSubmitting" class="submit-button">
          {{ isSubmitting ? 'Se salvează...' : 'Salvează' }}
        </button>
        <div v-if="editError" class="error-message">{{ editError }}</div>
      </form>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue';
import apiClient from '@/api.js';

const news = ref([]);
const isLoading = ref(false);
const error = ref('');
const showEditModal = ref(false);
const editForm = ref({
  id: null,
  title: '',
  content: '',
  image: null,
  imagePreview: null,
  is_published: false,
});
const isSubmitting = ref(false);
const editError = ref('');

const fetchNews = async () => {
  isLoading.value = true;
  error.value = '';
  try {
    const token = localStorage.getItem('token');
    const response = await apiClient.get('/my-news', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    news.value = response.data.map(item => {
      return {
        ...item,
        image: item.image ? `http://127.0.0.1:8000${item.image}` : null
      };
    });
  } catch (err) {
    error.value = err.response?.data?.error || 'Eroare la încărcarea știrilor.';
  } finally {
    isLoading.value = false;
  }
};

const deleteNews = async (newsId) => {
  if (!confirm('Sigur dorești să ștergi această știre?')) return;
  try {
    const token = localStorage.getItem('token');
    await apiClient.delete(`/news/${newsId}/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      data: {news_id: newsId}
    });
    news.value = news.value.filter(item => item.id !== newsId);
  } catch (err) {
    error.value = err.response?.data?.error || 'Eroare la ștergerea știrii.';
  }
};

const formatDate = (dateString) => {
  const [datePart, timePart] = dateString.split(' ');
  const [day, month, year] = datePart.split('/');
  const formattedDate = `${year}-${month}-${day}T${timePart}`;
  return new Date(formattedDate).toLocaleString('ro-RO');
};

const handleImageError = (item) => {
  console.log(`Image failed to load for item ${item.id}: ${item.image}`);
  item.image = '/placeholder.jpg';
};

const openEditModal = (item) => {
  editForm.value = {
    id: item.id,
    title: item.title,
    content: item.content,
    image: null,
    imagePreview: item.image,
    is_published: item.is_published,
  };
  showEditModal.value = true;
};

const closeEditModal = () => {
  showEditModal.value = false;
  editForm.value = {
    id: null,
    title: '',
    content: '',
    image: null,
    imagePreview: null,
    is_published: false,
  };
  editError.value = '';
};

const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    editForm.value.image = file;
    editForm.value.imagePreview = URL.createObjectURL(file);
  }
};

const updateNews = async () => {
  isSubmitting.value = true;
  editError.value = '';
  try {
    const token = localStorage.getItem('token');
    const formData = new FormData();
    formData.append('title', editForm.value.title);
    formData.append('content', editForm.value.content);
    formData.append('is_published', editForm.value.is_published);
    if (editForm.value.image) {
      formData.append('image', editForm.value.image);
    }

    const response = await apiClient.put(`/news/${editForm.value.id}/`, formData, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'multipart/form-data',
      },
    });

    const updatedNews = response.data;
    updatedNews.image = updatedNews.image ? `http://127.0.0.1:8000${updatedNews.image}` : null;
    const index = news.value.findIndex(item => item.id === updatedNews.id);
    if (index !== -1) {
      news.value[index] = updatedNews;
    }

    closeEditModal();
  } catch (err) {
    editError.value = err.response?.data?.error || 'Eroare la actualizarea știrii.';
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(fetchNews);
</script>

<style scoped>
h1 {
  text-align: center;
}

.news-list {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #1a202c;
  color: #e2e8f0;
  border-radius: 5px;
}

.news-item {
  padding: 15px;
  border-bottom: 1px solid #4a5568;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.news-image {
  max-width: 100%;
  height: auto;
  margin: 10px 0;
  width: 30%;
}

.delete-button, .edit-button {
  background-color: #e53e3e;
  color: #ffffff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  align-self: flex-start;
}

.buttons {
  display: flex;
}

.edit-button {
  background-color: #4299e1;
  margin-right: 10px;
}

.delete-button:hover {
  background-color: #c53030;
}

.edit-button:hover {
  background-color: #2b6cb0;
}

.error-message {
  color: #e53e3e;
  margin-top: 10px;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background-color: #fff;
  border-radius: 10px;
  padding: 20px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #2d3748;
}

.close-icon {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #718096;
  cursor: pointer;
}

.close-icon:hover {
  color: #e53e3e;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-group label {
  font-weight: 500;
  color: #2d3748;
}

.form-group input[type="text"],
.form-group textarea {
  padding: 8px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group textarea {
  resize: vertical;
}

.form-group input[type="file"] {
  padding: 5px 0;
}

.image-preview {
  max-width: 100%;
  height: auto;
  margin-top: 10px;
  border-radius: 4px;
}

.submit-button {
  background-color: #4299e1;
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  align-self: flex-end;
}

.submit-button:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

.submit-button:hover:not(:disabled) {
  background-color: #2b6cb0;
}
</style>