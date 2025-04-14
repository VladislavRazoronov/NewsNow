<template>
  <div class="news-by-category-page">
    <h1 class="title">Новини в категорії</h1>

    <div v-if="news.length > 0" class="news-list">
      <div
        v-for="newsItem in paginatedNews"
        :key="newsItem.id"
        class="news-item"
      >
        <img :src="getPhoto(newsItem)" alt="News Image" class="news-image" />
        <h2 class="news-title">{{ newsItem.title }}</h2>
        <p class="news-author">
          <i class="fas fa-user"></i> {{ newsItem.author_last_name }}
          {{ newsItem.author_first_name }}
          {{ newsItem.author_patronymic }}
        </p>
        <p class="news-category">
          <i class="fa-solid fa-list"></i> {{ newsItem.category_name }}
        </p>
        <p class="news-date">
          <i
            :class="
              getIcon(newsItem.date_of_creation, newsItem.date_of_last_update)
            "
          ></i>
          {{
            formatDate(newsItem.date_of_creation, newsItem.date_of_last_update)
          }}
        </p>
        <p class="news-description">
          {{ newsItem.text.slice(0, 150) }}...
          <router-link :to="`/news/${newsItem.id}`" class="read-more">
            Читати далі
          </router-link>
        </p>
      </div>
    </div>

    <div class="pagination" v-if="totalPages > 1">
      <button @click="changePage(page - 1)" :disabled="page === 1">
        &laquo;
      </button>
      <span>Сторінка {{ page }} з {{ totalPages }}</span>
      <button @click="changePage(page + 1)" :disabled="page === totalPages">
        &raquo;
      </button>
    </div>

    <div v-else>
      <p v-if="news.length === 0">Новин не знайдено в цій категорії.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      news: [],
      page: 1,
      newsPerPage: 9,
      categoryId: this.$route.params.id,
    };
  },
  watch: {
    "$route.params.id": {
      handler(newId) {
        this.categoryId = newId;
        this.fetchNewsByCategory();
      },
      immediate: true,
    },
  },

  mounted() {
    this.fetchNewsByCategory();
  },
  computed: {
    totalPages() {
      return Math.ceil(this.news.length / this.newsPerPage);
    },
    paginatedNews() {
      const startIndex = (this.page - 1) * this.newsPerPage;
      const endIndex = startIndex + this.newsPerPage;
      return this.news.slice(startIndex, endIndex);
    },
  },
  methods: {
    getPhoto(newsItem) {
      try {
        const photoPath = newsItem.image.split("media/images/news_images/")[1];
        if (!photoPath) throw new Error("Invalid image path");

        const decodedFileName = decodeURIComponent(photoPath.split("/").pop());

        return require(`@/../../backend/media/images/news_images/${decodedFileName}`);
      } catch (error) {
        console.error("Error loading photo:", error);
        return "";
      }
    },

    async fetchNewsByCategory() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/news/news_by_category/",
          {
            news_category_id: this.categoryId,
          }
        );

        if (response.status === 200 && response.data.news_list?.length > 0) {
          this.news = response.data.news_list;
          console.log(this.news);
        } else {
          console.warn("Новини не знайдено в цій категорії.");
          this.news = [];
        }
      } catch (error) {
        if (error.response?.status === 404) {
          console.warn("Новини не знайдено.");
        } else {
          console.error("Помилка завантаження новин:", error);
        }
        this.news = [];
      }
    },
    changePage(newPage) {
      if (newPage >= 1 && newPage <= this.totalPages) {
        this.page = newPage;
      }
    },
    getIcon(dateOfCreation, dateOfLastUpdate) {
      return new Date(dateOfCreation).getTime() ===
        new Date(dateOfLastUpdate).getTime()
        ? "fa fa-calendar"
        : "fa fa-edit";
    },
    formatDate(dateOfCreation, dateOfLastUpdate) {
      const createdDate = new Date(dateOfCreation);
      const updatedDate = new Date(dateOfLastUpdate);

      if (createdDate.getTime() === updatedDate.getTime()) {
        return createdDate.toLocaleDateString("uk-UA", {
          year: "numeric",
          month: "long",
          day: "numeric",
          hour: "numeric",
          minute: "numeric",
        });
      } else {
        return `Ред. ${updatedDate.toLocaleDateString("uk-UA", {
          year: "numeric",
          month: "long",
          day: "numeric",
          hour: "numeric",
          minute: "numeric",
        })}`;
      }
    },
  },
};
</script>

<style scoped>
.news-image {
  width: 320px;
  height: 180px;
  object-fit: cover;
}

i {
  font-size: 16px;
  color: black;
  width: 20px;
  text-align: center;
}
.news-by-category-page {
  font-family: Arial, sans-serif;
  background-color: #f4f4f9;
  color: #333;
  padding: 40px 20px;
  margin-bottom: 10px;
  text-align: center;
}

.title {
  font-size: 32px;
  margin-bottom: 20px;
}

.news-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  max-width: 1100px;
  margin: 0 auto;
}

.news-item {
  background: white;
  color: black;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: left;
  transition: transform 0.3s, box-shadow 0.3s;
}

.news-item:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.news-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
  min-height: 70px;
}

.news-author,
.news-category,
.news-date {
  font-size: 14px;
  color: #555;
  margin-bottom: 8px;
}

.news-description {
  font-size: 16px;
  color: #666;
  text-align: justify;
  line-height: 1.5;
}

.read-more {
  display: inline-block;
  color: #0066cc;
  text-decoration: none;
}

.read-more:hover {
  text-decoration: underline;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination button {
  padding: 8px 12px;
  margin: 0 5px;
  border: none;
  background-color: #00274d;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination span {
  font-size: 16px;
  margin: 0 10px;
}
</style>
