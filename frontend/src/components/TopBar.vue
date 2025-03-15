<script setup>
import {ref, computed, onMounted, onUnmounted} from 'vue';
import {useRouter} from 'vue-router';

const router = useRouter();
const isDropdownOpen = ref(false);
const authToken = ref(localStorage.getItem('token'));

const isAuthenticated = computed(() => !!authToken.value);

const checkTokenStatus = () => {
  authToken.value = localStorage.getItem('token');
};

const goToAllNews = () => router.push('/');
const goToCreateNews = () => router.push('/create-news');
const goToMyNews = () => router.push('/my-news');
const goToSignIn = () => router.push('/auth');
const goToSavedNews = () => router.push('/saved-news');

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};

const logout = () => {
  localStorage.removeItem('token');
  authToken.value = null;
  isDropdownOpen.value = false;
  router.push('/auth');
};

onMounted(() => {
  window.addEventListener('storage', checkTokenStatus);
  const intervalId = setInterval(checkTokenStatus, 1000);

  onUnmounted(() => {
    window.removeEventListener('storage', checkTokenStatus);
    clearInterval(intervalId);
  });
});
</script>

<template>
  <nav class="top-bar">
    <div class="left-section">
      <button @click="goToAllNews" class="nav-button">Toate știrile</button>
      <button v-if="isAuthenticated" @click="goToCreateNews" class="nav-button">Creează o știre</button>
      <button v-if="isAuthenticated" @click="goToMyNews" class="nav-button">Știrile mele</button>
      <button v-if="isAuthenticated" @click="goToSavedNews" class="nav-button">Știrile salvate</button>
    </div>

    <div class="right-section">
      <div v-if="isAuthenticated">
        <button class="user-icon" @click="toggleDropdown">
          <i class="fas fa-user"></i>
        </button>
        <div v-if="isDropdownOpen" class="dropdown">
          <button @click="router.push('/profile')" class="dropdown-item">Profil</button>
          <button @click="logout" class="dropdown-item">Logout</button>
        </div>
      </div>

      <button v-else class="sign-in-icon" @click="goToSignIn">
        <i class="fas fa-sign-in-alt"></i>
      </button>
    </div>
  </nav>
</template>

<style scoped>
.top-bar {
  position: fixed;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #1a202c;
  padding: 10px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  top: 0;
  left: 0;
  right: 0;
  z-index: 1;
}

.left-section {
  display: flex;
  gap: 15px;
}

.nav-button {
  background: none;
  border: none;
  color: #e2e8f0;
  font-size: 16px;
  padding: 8px 16px;
  cursor: pointer;
  transition: color 0.3s;
}

.nav-button:hover {
  color: #63b3ed;
}

.right-section {
  position: relative;
}

.user-icon,
.sign-in-icon {
  background: none;
  border: none;
  color: #e2e8f0;
  font-size: 20px;
  cursor: pointer;
  padding: 8px;
}

.user-icon:hover,
.sign-in-icon:hover {
  color: #63b3ed;
}

.dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: #2d3748;
  border-radius: 4px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  min-width: 120px;
}

.dropdown-item {
  display: block;
  width: 100%;
  background: none;
  border: none;
  color: #e2e8f0;
  padding: 8px 16px;
  text-align: left;
  cursor: pointer;
  font-size: 14px;
}

.dropdown-item:hover {
  background-color: #4a5568;
}
</style>