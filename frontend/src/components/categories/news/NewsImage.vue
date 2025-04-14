<template>
  <img :src="imageUrl" alt="News Image" class="news-image" />
</template>

<script>
export default {
  props: {
    imageUrl: String,
  },
};
</script>
