<template>
  <div class="container">
    <div class="title">Easy Recipes</div>
    <nav class="content">
      <router-link to="/recipes/" class="content-link"> Recipes </router-link>
      <router-link to="/ingredients/" class="content-link"> Ingredients </router-link>
    </nav>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.container {
  display: flex;
  padding-bottom: 10px;
  border-bottom: 2px solid #ddd;
}

.title {
  width: 180px;
  font-size: 30px;
  font-weight: 800;
  background-color: #bcc0cc;
  padding: 5px;
  text-align: center;
}

.content {
  display: flex;
  padding-left: 30px;
}

.content-link {
  display: flex;
  padding-left: 30px;
  height: 100%;
  font-size: 20px;
  text-decoration: none;
  position: relative;
  align-items: center;
  padding: 0 10px;
}

.content-link:hover {
  background-color: #eee;
}
</style>
