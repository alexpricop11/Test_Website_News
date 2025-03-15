<script setup>
import {ref, onMounted, onUnmounted} from 'vue';
import apiClient from '@/api.js';

const savedNews = ref([]);
const isLoading = ref(false);
const error = ref('');
const selectedNews = ref(null);
const isSaving = ref(false);

const fetchSavedNews = async () => {
  isLoading.value = true;
  error.value = '';
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      new Error('Nu ești autentificat. Te rugăm să te loghezi.');
    }
    const response = await apiClient.get('/saved-news/', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    console.log("Response from /saved-news:", response.data);
    if (!response.data || !Array.isArray(response.data)) {
      new Error('Răspuns invalid de la server.');
    }
    savedNews.value = response.data.map(item => ({
      id: item.id,
      news_title: item.news_title,
      news: {
        id: item.news.id,
        title: item.news.title,
        content: item.news.content,
        image: item.news.image ? `http127.0.0.1:8000${item.news.image}` : null,
        user: {
          username: item.user.username,
        },
        published_at: item.news.published_at || new Date().toISOString(),
      },
      saved_at: item.saved_at || new Date().toISOString(),
    }));
  } catch (err) {
    error.value = err.response?.data?.error || err.message || 'Eroare la încărcarea știrilor salvate.';
    console.error("Fetch error:", err.response ? err.response.data : err);
  } finally {
    isLoading.value = false;
  }
};

const handleImageError = (item) => {
  console.log(`Image failed to load: ${item.image}`);
  item.image = '/placeholder.jpg';
};

const formatDate = (dateString) => {
  if (!dateString || dateString === 'null') {
    return 'N/A';
  }
  const date = new Date(dateString);
  return isNaN(date.getTime()) ? 'N/A' : date.toLocaleString('ro-RO');
};

const openModal = (item) => {
  selectedNews.value = item;
};

const closeModal = () => {
  selectedNews.value = null;
};

// Funcționalitate pentru desalvare
const unsaveNews = async (item) => {
  isSaving.value = true;
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      new Error('Nu ești autentificat. Te rugăm să te loghezi.');
    }
    await apiClient.delete('/saved-news/', {
      headers: {Authorization: `Bearer ${token}`},
      data: {news_id: item.news.id},
    });
    savedNews.value = savedNews.value.filter(news => news.id !== item.id);
    if (selectedNews.value && selectedNews.value.id === item.id) {
      closeModal();
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Eroare la desalvarea știrii.';
    console.error("Unsave error:", err);
  } finally {
    isSaving.value = false;
  }
};

onMounted(() => {
  fetchSavedNews();
  window.addEventListener('focus', fetchSavedNews);
});

onUnmounted(() => {
  window.removeEventListener('focus', fetchSavedNews);
});
</script>

<template>
  <div class="container">
    <h1>Știri salvate</h1>
    <div v-if="isLoading" class="loading">
      <i class="fas fa-spinner fa-spin"></i> Se încarcă știrile salvate...
    </div>
    <div v-else-if="savedNews.length === 0" class="no-news">
      Nu ai știri salvate momentan.
    </div>
    <div v-else class="news-list">
      <div v-for="item in savedNews" :key="item.id" class="news-card">
        <h2 @click="openModal(item)" class="news-title">{{ item.news_title }}</h2>
        <p class="author"><i class="fas fa-user-circle"></i> {{ item.news.user?.username || 'Unknown' }}</p>
        <p class="content">
          {{
            (item.news.content || '').slice(0, 100) + (item.news.content && item.news.content.length > 100 ? '...' : '')
          }}
        </p>
        <img v-if="item.news.image" :src="item.news.image" alt="News Image" class="news-image"
             @error="handleImageError(item)"/>
        <div class="meta">
          <p><i class="fas fa-calendar-day"></i> Salvat la: {{ formatDate(item.saved_at) }}</p>
          <p><i class="fas fa-calendar-day"></i> Publicat la: {{ formatDate(item.news.published_at) }}</p>
        </div>
        <button class="unsave-btn" @click="unsaveNews(item)" :disabled="isSaving">
          <i class="fas fa-bookmark"></i> Desalvează
        </button>
      </div>
    </div>

    <!-- Modal pentru detalii -->
    <div v-if="selectedNews" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h2>{{ selectedNews.news_title }}</h2>
        <p class="author"><i class="fas fa-user-circle"></i> {{ selectedNews.news.user?.username || 'Unknown' }}</p>
        <img v-if="selectedNews.news.image" :src="selectedNews.news.image" alt="News Image" class="modal-image"
             @error="handleImageError(selectedNews)"/>
        <p class="full-content">{{ selectedNews.news.content }}</p>
        <div class="meta">
          <p><i class="fas fa-calendar-day"></i> Salvat la: {{ formatDate(selectedNews.saved_at) }}</p>
          <p><i class="fas fa-calendar-day"></i> Publicat la: {{ formatDate(selectedNews.news.published_at) }}</p>
        </div>
        <button class="unsave-btn" @click="unsaveNews(selectedNews)" :disabled="isSaving">
          <i class="fas fa-bookmark"></i> Desalvează
        </button>
        <button class="close-btn" @click="closeModal">Închide</button>
      </div>
    </div>

    <div v-if="error" class="error-message">{{ error }}</div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 50px 20px;
  min-height: 100vh;
}

h1 {
  text-align: center;
  font-size: 3rem;
  color: #2b6cb0;
  margin-bottom: 50px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
}

.news-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
}

.loading {
  text-align: center;
  font-size: 1.3rem;
  color: #4a5568;
  padding: 30px;
}

.loading i {
  margin-right: 10px;
}

.no-news {
  text-align: center;
  font-size: 1.3rem;
  color: #718096;
  padding: 30px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.news-card {
  background-color: #1a202c;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.news-card:hover {
  transform: scale(1.03);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
}

.news-title {
  font-size: 1.6rem;
  color: #ffffff;
  margin-bottom: 12px;
  font-weight: 600;
  cursor: pointer;
}

.news-title:hover {
  color: #4299e1;
}

.author {
  font-size: 0.95rem;
  color: #718096;
  margin-bottom: 12px;
}

.author i {
  margin-right: 8px;
  color: #4299e1;
}

.content {
  font-size: 1rem;
  color: #e2e8f0;
  line-height: 1.6;
  margin-bottom: 15px;
}

.news-image {
  max-width: 100%;
  height: auto;
  width: 50%;
  border-radius: 10px;
  margin: 15px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 0.9rem;
  color: #718096;
}

.meta i {
  margin-right: 6px;
}

.unsave-btn {
  background-color: #e53e3e;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.3s ease;
}

.unsave-btn:hover {
  background-color: #c53030;
}

.unsave-btn:disabled {
  background-color: #718096;
  cursor: not-allowed;
}

/* Stiluri pentru modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #1a202c;
  padding: 30px;
  border-radius: 15px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.modal-content h2 {
  font-size: 2rem;
  color: #ffffff;
  margin-bottom: 20px;
}

.modal-image {
  max-width: 100%;
  height: auto;
  border-radius: 10px;
  margin: 15px 0;
}

.full-content {
  font-size: 1.1rem;
  color: #e2e8f0;
  line-height: 1.8;
  margin-bottom: 20px;
}

.close-btn {
  background-color: #4299e1;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  margin-top: 10px;
  transition: background-color 0.3s ease;
}

.close-btn:hover {
  background-color: #2b6cb0;
}

.error-message {
  text-align: center;
  color: #fff;
  background-color: #e53e3e;
  font-weight: 500;
  margin-top: 25px;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .news-list {
    grid-template-columns: 1fr;
  }

  h1 {
    font-size: 2.2rem;
  }

  .news-card h2 {
    font-size: 1.4rem;
  }

  .modal-content {
    width: 95%;
    padding: 20px;
  }
}
</style>