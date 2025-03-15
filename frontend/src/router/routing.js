import {createRouter, createWebHistory} from 'vue-router';
import AuthPage from '@/views/AuthPage.vue';
import CreateNews from "@/views/CreateNews.vue";
import MyNews from "@/views/MyNews.vue";
import AllNews from "@/views/AllNews.vue";
import Profile from "@/components/Profile.vue";
import SavedNews from "@/views/SavedNews.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/', component: AllNews},
        {path: '/auth', component: AuthPage},
        {path: '/profile', component: Profile},
        {path: '/create-news', component: CreateNews},
        {path: '/my-news', component: MyNews},
        {path: '/saved-news', component: SavedNews},
    ]
});

export default router;