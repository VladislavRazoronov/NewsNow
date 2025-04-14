<template>
  <div class="categories-page">
    <h1 class="title">Категорії новин</h1>
    <div class="categories-grid">
      <router-link
        v-for="category in categories"
        :key="category.id"
        :to="`/categories_news/${category.id}`"
        class="category-card"
      >
        <img
          :src="getPhoto(category)"
          :alt="category.category_name"
          class="category-image"
        />

        <h2 class="category-name">{{ category.category_name }}</h2>
      </router-link>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      categories: [],
    };
  },
  mounted() {
    this.fetchCategories();
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/news/news_categories/"
        );

        if (
          response.status === 200 &&
          response.data.news_categories_list?.length > 0
        ) {
          this.categories = response.data.news_categories_list;
        } else {
          console.warn("Категорії новин не знайдено.");
          this.categories = [];
        }
      } catch (error) {
        if (error.response?.status === 404) {
          console.warn("Категорії новин відсутні.");
        } else {
          console.error("Помилка завантаження категорій:", error);
        }
        this.categories = [];
      }
    },
    getPhoto(category) {
      try {
        const photoPath = category.category_image.split(
          "media/images/news_category_images/"
        )[1];
        if (!photoPath) throw new Error("Invalid image path");

        const decodedFileName = decodeURIComponent(photoPath.split("/").pop());
        return require(`@/../../backend/media/images/news_category_images/${decodedFileName}`);
      } catch (error) {
        console.error("Error loading photo:", error);
        return "";
      }
    },
  },
};
</script>

<style scoped>
.categories-page {
  font-family: Arial, sans-serif;
  background-color: #00274d;
  color: #fff;
  text-align: center;
  padding: 40px 20px;
  margin-bottom: 10px;
}

.title {
  font-size: 32px;
  margin-bottom: 20px;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 30px;
  max-width: 1100px;
  margin: 0 auto;
}

.category-card {
  display: block;
  background: white;
  color: black;
  border-radius: 10px;
  padding: 15px;
  text-align: center;
  text-decoration: none;
  transition: transform 0.3s, background 0.3s;
}

.category-card:hover {
  transform: scale(1.1);
  background: #f0f0f0;
}

.category-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 10px;
}

.category-name {
  margin: 10px 0 0;
  font-size: 18px;
  font-weight: bold;
}
</style>
