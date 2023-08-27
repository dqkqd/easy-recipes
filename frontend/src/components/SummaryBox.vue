<template>
  <div class="box">
    <div class="title">{{ props.recipe.name }}</div>
    <img class="img" v-if="props.recipe.image_uri" :src="image_uri" />
  </div>
</template>

<script setup lang="ts">
import { convertFileServerDev } from '@/env';
import { computed } from 'vue';

const props = defineProps(['recipe']);
const image_uri = computed(() => {
  return convertFileServerDev(props.recipe.image_uri);
});
</script>

<style scoped>
.title {
  font-size: 1.5rem;
  margin: 5px;
  font-weight: bold;
  text-align: center;
}

.box {
  width: 200px;
  height: 200px;
  border: 1px solid;
  transition: transform 0.2s;
  margin: 5px;
}

.bigger-box {
  width: 500px;
  height: 500px;
}

.box:hover {
  box-shadow: 5px 5px 5px #eee;
  transform: scale(1.2);
}

.img {
  width: 150px;
  height: 150px;
  margin: auto;
  display: block;
}
</style>
