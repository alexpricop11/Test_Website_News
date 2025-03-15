<script setup>
import TopBar from "@/components/TopBar.vue";
</script>

<template>
  <div>
    <TopBar/>
  </div>
  <div>
    <router-view/>
  </div>
</template>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background-color: black;
  color: white;
}
</style>
