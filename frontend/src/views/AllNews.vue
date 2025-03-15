<template>
  <div class="container">
    <h1>Toate știrile</h1>
    <div class="news-list">
      <div v-if="isLoading" class="loading">
        <i class="fas fa-spinner fa-spin"></i> Se încarcă știrile...
      </div>
      <div v-else-if="news.length === 0" class="no-news">Nu există știri disponibile momentan.</div>
      <ul v-else>
        <li v-for="item in news" :key="item.id" class="news-card">
          <h2>{{ item.title || 'Titlu indisponibil' }}</h2>
          <p class="author"><i class="fas fa-user-circle"></i> {{ item.author?.username || 'Autor necunoscut' }}</p>
          <p class="content">
            {{
              (item.content || 'Conținut indisponibil').slice(0, 100) + (item.content && item.content.length > 100 ? '...' : '')
            }}
          </p>
          <div class="buttons">
            <button @click="openModal(item)" class="details-button">
              <i class="fas fa-eye"></i> Detalii
            </button>
            <button v-if="!item.is_saved" @click="toggleSaveNews(item)" class="save-button" :disabled="isSaving">
              <i class="far fa-bookmark"></i> Salvează
            </button>
            <button v-else @click="toggleSaveNews(item)" class="save-button saved" :disabled="isSaving">
              <i class="fas fa-bookmark"></i> Desalvează
            </button>
          </div>
          <img v-if="item.image" :src="item.image" alt="News Image" class="news-image" @error="handleImageError(item)"/>
          <div class="meta">
            <p><i class="fas fa-calendar-day"></i> {{ formatDate(item.published_at) }}</p>
            <span class="status" :class="{ published: item.is_published }">
              <i :class="item.is_published ? 'fas fa-check' : 'fas fa-times'"></i>
              {{ item.is_published ? 'Publicat' : 'Nepublicat' }}
            </span>
          </div>
        </li>
      </ul>
      <div v-if="error" class="error-message">{{ error }}</div>
    </div>

    <div v-if="selectedNews" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ selectedNews.title || 'Titlu indisponibil' }}</h2>
          <button @click="closeModal" class="close-icon">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <p class="author"><i class="fas fa-user-circle"></i> {{ selectedNews.author?.username || 'Autor necunoscut' }}
        </p>
        <p class="content">{{ selectedNews.content || 'Conținut indisponibil' }}</p>
        <button v-if="!selectedNews.is_saved" @click="toggleSaveNews(selectedNews)" class="save-button"
                :disabled="isSaving">
          <i class="far fa-bookmark"></i> Salvează
        </button>
        <button v-else @click="toggleSaveNews(selectedNews)" class="save-button saved" :disabled="isSaving">
          <i class="fas fa-bookmark"></i> Desalvează
        </button>
        <img v-if="selectedNews.image" :src="selectedNews.image" alt="News Image" class="modal-image"
             @error="handleImageError(selectedNews)"/>
        <div class="meta">
          <p><i class="fas fa-calendar-day"></i> {{ formatDate(selectedNews.published_at) }}</p>
          <span class="status" :class="{ published: selectedNews.is_published }">
            <i :class="selectedNews.is_published ? 'fas fa-check' : 'fas fa-times'"></i>
          </span>
        </div>

        <div class="comment-form">
          <textarea v-model="newComment" placeholder="Adaugă un comentariu..." rows="3"></textarea>
          <button @click="submitComment" :disabled="isSubmitting || !newComment.trim()" class="submit-button">
            <i class="fas fa-paper-plane"></i> {{ isSubmitting ? 'Se trimite...' : 'Trimite' }}
          </button>
          <div v-if="commentError" class="comment-error">{{ commentError }}</div>
        </div>

        <div class="comments-section">
          <h3>Comentarii</h3>
          <div v-if="isLoadingComments" class="loading">
            <i class="fas fa-spinner fa-spin"></i> Se încarcă comentariile...
          </div>
          <div v-else-if="comments.length === 0" class="no-comments">Nu există comentarii momentan.</div>
          <ul v-else class="comment-list">
            <li v-for="comment in comments" :key="comment.id" class="comment">
              <p class="comment-content">{{ comment.content || 'Comentariu indisponibil' }}</p>
              <p class="comment-meta">
                <i class="fas fa-user"></i> {{ comment.user?.username || 'Utilizator necunoscut' }} -
                <i class="fas fa-calendar-day"></i> {{ formatDate(comment.created_at) }}
              </p>
              <button
                  v-if="comment.user?.id === currentUserId"
                  @click="deleteComment(comment.id)"
                  class="delete-comment-button"
                  :disabled="isDeleting === comment.id"
              >
                <i class="fas fa-trash"></i> {{ isDeleting === comment.id ? 'Se șterge...' : 'Șterge' }}
              </button>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted} from 'vue';
import apiClient from '@/api.js';
import {jwtDecode} from 'jwt-decode';

const news = ref([]);
const isLoading = ref(false);
const error = ref('');
const selectedNews = ref(null);
const comments = ref([]);
const isLoadingComments = ref(false);
const newComment = ref('');
const commentError = ref('');
const isSubmitting = ref(false);
const isSaving = ref(false);
const isDeleting = ref(null);
const currentUserId = ref(null);

const getCurrentUserId = () => {
  const token = localStorage.getItem('token');
  if (token) {
    try {
      const decodedToken = jwtDecode(token);
      currentUserId.value = decodedToken.user_id;
    } catch (err) {
      console.error('Invalid token:', err);
    }
  }
};

const fetchAllNews = async () => {
  isLoading.value = true;
  error.value = '';
  try {
    const token = localStorage.getItem('token');
    if (!token) new Error('Nu ești autentificat.');

    const response = await apiClient.get('/news/', {
      headers: {Authorization: `Bearer ${token}`},
    });

    news.value = response.data.map(item => {
      return {
        ...item,
        image: item.image && item.image.trim() ?
            (item.image.startsWith('http') ? item.image : `http://127.0.0.1:8000${item.image}`) :
            null
      };
    });
  } catch (err) {
    error.value = err.response?.data?.error || 'Eroare la încărcarea știrilor.';
    console.error('Fetch all news error:', err.response ? err.response.data : err);
  } finally {
    isLoading.value = false;
  }
};


const toggleSaveNews = async (item) => {
  isSaving.value = true;
  try {
    const token = localStorage.getItem('token');
    if (!token) new Error('Nu ești autentificat. Te rugăm să te loghezi.');

    const wasSaved = item.is_saved;
    item.is_saved = !item.is_saved;

    if (selectedNews.value && selectedNews.value.id === item.id) {
      selectedNews.value.is_saved = item.is_saved;
    }

    let response;
    if (wasSaved) {
      response = await apiClient.delete('/saved-news/', {
        headers: {Authorization: `Bearer ${token}`},
        data: {news_id: item.id},
      });
      console.log('Unsave response:', response.data);
    } else {
      response = await apiClient.post('/saved-news/', {news_id: item.id}, {
        headers: {Authorization: `Bearer ${token}`},
      });
      console.log('Save response:', response.data);
    }

    item.is_saved = response.data.data?.is_saved ?? !wasSaved;
    if (selectedNews.value && selectedNews.value.id === item.id) {
      selectedNews.value.is_saved = item.is_saved;
    }
  } catch (err) {
    item.is_saved = !item.is_saved;
    if (selectedNews.value && selectedNews.value.id === item.id) {
      selectedNews.value.is_saved = item.is_saved;
    }
    error.value = err.response?.data?.error || 'Eroare la salvarea/desalvarea știrii.';
    console.error('Toggle save error:', err.response ? err.response.data : err);
  } finally {
    isSaving.value = false;
  }
};

const fetchComments = async (newsId) => {
  isLoadingComments.value = true;
  commentError.value = '';
  try {
    const token = localStorage.getItem('token');
    if (!token) new Error('Nu ești autentificat.');

    const response = await apiClient.get(`/comments/?news_id=${newsId}`, {
      headers: {Authorization: `Bearer ${token}`},
    });

    console.log('Fetch comments response:', response.data);
    comments.value = response.data;
  } catch (err) {
    commentError.value = err.response?.data?.error || 'Eroare la încărcarea comentariilor.';
    console.error('Fetch comments error:', err.response ? err.response.data : err);
  } finally {
    isLoadingComments.value = false;
  }
};

const submitComment = async () => {
  if (!newComment.value.trim()) return;

  isSubmitting.value = true;
  commentError.value = '';
  try {
    const token = localStorage.getItem('token');
    if (!token) new Error('Nu ești autentificat.');

    let userId;
    try {
      const decodedToken = jwtDecode(token);
      userId = decodedToken.user_id;
    } catch (err) {
      new Error('Token invalid. Te rugăm să te loghezi din nou.');
    }

    const response = await apiClient.post(
        '/comments/',
        {
          news: selectedNews.value.id,
          content: newComment.value,
          user_id: userId,
        },
        {
          headers: {Authorization: `Bearer ${token}`},
        }
    );

    console.log('Submit comment response:', response.data);
    comments.value.push(response.data);
    newComment.value = '';
  } catch (err) {
    commentError.value = err.response?.data?.content?.[0] || err.response?.data?.error || 'Eroare la adăugarea comentariului.';
    console.error('Submit comment error:', err.response ? err.response.data : err);
  } finally {
    isSubmitting.value = false;
  }
};

const deleteComment = async (commentId) => {
  if (!confirm('Sigur dorești să ștergi acest comentariu?')) return;

  isDeleting.value = commentId;
  try {
    const token = localStorage.getItem('token');
    if (!token) new Error('Nu ești autentificat.');

    await apiClient.delete('/comments/', {
      headers: {Authorization: `Bearer ${token}`},
      data: {comment_id: commentId},
    });

    comments.value = comments.value.filter(comment => comment.id !== commentId);
  } catch (err) {
    commentError.value = err.response?.data?.error || 'Eroare la ștergerea comentariului.';
    console.error('Delete comment error:', err.response ? err.response.data : err);
  } finally {
    isDeleting.value = null;
  }
};

const openModal = (item) => {
  selectedNews.value = {...item};
  fetchComments(item.id);
};

const closeModal = () => {
  selectedNews.value = null;
  comments.value = [];
  newComment.value = '';
  commentError.value = '';
  isSubmitting.value = false;
};

const formatDate = (dateString) => {
  if (!dateString || dateString === 'null') {
    return 'N/A';
  }

  try {
    let date;
    if (dateString.includes('/')) {
      const [datePart, timePart] = dateString.split(' ');
      const [day, month, year] = datePart.split('/');
      const formattedDate = `${year}-${month}-${day}T${timePart || '00:00:00'}`;
      date = new Date(formattedDate);
    } else {
      date = new Date(dateString);
    }

    return isNaN(date.getTime()) ? 'N/A' : date.toLocaleString('ro-RO');
  } catch (err) {
    console.error('Error formatting date:', dateString, err);
    return 'N/A';
  }
};

const handleImageError = (item) => {
  console.log(`Image failed to load: ${item.image}`);
  item.image = '/placeholder.jpg';
};

onMounted(() => {
  getCurrentUserId();
  fetchAllNews();
});
</script>

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
  grid-column: span 2;
  text-align: center;
  font-size: 1.3rem;
  color: #4a5568;
  padding: 30px;
}

.loading i {
  margin-right: 10px;
}

.no-news {
  grid-column: span 2;
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

.news-card h2 {
  font-size: 1.6rem;
  color: #ffffff;
  margin-bottom: 12px;
  font-weight: 600;
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
  color: #4a5568;
  line-height: 1.6;
  margin-bottom: 15px;
}

.details-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(90deg, #4299e1, #63b3ed);
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 25px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.details-button:hover {
  background: linear-gradient(90deg, #2b6cb0, #4299e1);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.save-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(90deg, #48bb78, #68d391);
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 25px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.3s ease;
  margin-left: 10px;
}

.save-button.saved {
  background: linear-gradient(90deg, #2f855a, #38a169);
}

.save-button:hover:not(:disabled) {
  background: linear-gradient(90deg, #2f855a, #38a169);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.save-button:disabled {
  background: #a0aec0;
  cursor: not-allowed;
  opacity: 0.7;
}

.buttons {
  display: flex;
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
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  color: #718096;
}

.meta i {
  margin-right: 6px;
}

.status {
  display: flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 12px;
}

.status.published {
  background-color: #c6f6d5;
  color: #2f855a;
}

.status:not(.published) {
  background-color: #fed7d7;
  color: #c53030;
}

.error-message {
  grid-column: span 2;
  text-align: center;
  color: #fff;
  background-color: #e53e3e;
  font-weight: 500;
  margin-top: 25px;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Modal styles */
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
  backdrop-filter: blur(3px);
}

.modal {
  background-color: #fff;
  border-radius: 20px;
  padding: 30px;
  max-width: 700px;
  width: 90%;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  position: relative;
  animation: slideIn 0.4s ease;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal h2 {
  font-size: 2rem;
  color: #2d3748;
  font-weight: 600;
}

.close-icon {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #718096;
  cursor: pointer;
  transition: color 0.3s ease;
}

.close-icon:hover {
  color: #e53e3e;
}

.modal .author {
  font-size: 1rem;
  color: #718096;
}

.modal .content {
  font-size: 1.15rem;
  color: #4a5568;
  line-height: 1.7;
  margin: 20px 0;
}

.modal-image {
  max-width: 100%;
  height: auto;
  border-radius: 12px;
  margin: 20px 0;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.comments-section {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

.comments-section h3 {
  font-size: 1.5rem;
  color: #2b6cb0;
  margin-bottom: 20px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.no-comments {
  font-size: 1rem;
  color: #718096;
  padding: 15px;
  text-align: center;
  background-color: #f7fafc;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.comment-list {
  list-style: none;
  padding: 0;
  max-height: 300px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #4299e1 #e2e8f0;
}

.comment {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 15px 20px;
  margin-bottom: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.06);
  border-left: 4px solid #4299e1;
}

.comment-content {
  font-size: 1rem;
  color: #2d3748;
  margin-bottom: 8px;
  line-height: 1.5;
}

.comment-meta {
  font-size: 0.85rem;
  color: #718096;
  display: flex;
  align-items: center;
  gap: 10px;
}

.comment-form {
  margin-top: 25px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.comment-form textarea {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 1rem;
  resize: none;
  outline: none;
  background-color: #f7fafc;
}

.submit-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: linear-gradient(90deg, #4299e1, #63b3ed);
  color: #fff;
  border: none;
  padding: 12px 25px;
  border-radius: 25px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  align-self: flex-end;
}

.submit-button:disabled {
  background: #a0aec0;
  cursor: not-allowed;
  opacity: 0.7;
}

.comment-error {
  color: #e53e3e;
  font-size: 0.9rem;
  font-weight: 500;
  margin-top: 10px;
  background-color: #fed7d7;
  padding: 8px 12px;
  border-radius: 8px;
}

.delete-comment-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(90deg, #e53e3e, #f56565);
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 25px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.delete-comment-button:hover:not(:disabled) {
  background: linear-gradient(90deg, #c53030, #e53e3e);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.delete-comment-button:disabled {
  background: #a0aec0;
  cursor: not-allowed;
  opacity: 0.7;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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

  .modal h2 {
    font-size: 1.6rem;
  }

  .modal {
    padding: 20px;
    width: 95%;
  }

  .comments-section h3 {
    font-size: 1.3rem;
  }

  .submit-button {
    width: 100%;
    justify-content: center;
  }
}
</style>