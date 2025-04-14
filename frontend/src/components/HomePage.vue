<template>
  <div class="home-page">
    <section class="hero">
      <div class="hero-content">
        <h1>Ласкаво просимо на портал новин міста Стрий</h1>
        <p>
          Дізнавайся про останні події в регіоні, найактуальніші новини
          політики, економіки, спорту та культури. Залишайся в курсі подій разом
          з нами!
        </p>
      </div>
    </section>

    <section class="news-section">
      <div class="categories">
        <router-link
          v-for="category in categories"
          :key="category.id"
          :to="`/categories_news/${category.id}`"
          class="category-link"
          >{{ category.category_name }}</router-link
        >
      </div>

      <h2>Останні новини</h2>
      <div v-if="news.length > 0" class="news-list">
        <div v-for="newsItem in news" :key="newsItem.id" class="news-item">
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
              formatDate(
                newsItem.date_of_creation,
                newsItem.date_of_last_update
              )
            }}
          </p>
          <p class="news-description">
            {{ newsItem.text.slice(0, 150) }}...
            <router-link :to="`/news/${newsItem.id}`" class="read-mores">
              Читати далі
            </router-link>
          </p>
        </div>
      </div>
    </section>

    <section class="gallery">
      <galleryComp />
    </section>

    <section class="cta">
      <h2>Реєструйся та будь в курсі новин регіону!</h2>
      <router-link to="/login" class="cta-button">Зареєструватися</router-link>
    </section>
  </div>
</template>

<script>
import axios from "axios";

import galleryComp from "./galleryComp.vue";
export default {
  components: { galleryComp },
  data() {
    return {
      categories: [],
      news: [],
      highlightedPosts: [
        {
          id: 6,
          title: "Цікавий пост",
          author: "Автор 6",
          date: "2025-03-01",
          image: require("@/assets/hero.png"),
        },
      ],
    };
  },
  mounted() {
    this.fetchCategories();
    this.fetchNews();
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
    async fetchNews() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/news/last_six_news_info/"
        );

        if (
          response.status === 200 &&
          response.data.last_six_news_info?.length > 0
        ) {
          this.news = response.data.last_six_news_info;
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

.news-image {
  width: 320px;
  height: 180px;
  object-fit: cover;
}

.read-mores {
  display: inline-block;
  color: #0066cc;
  text-decoration: none;
}

.read-mores:hover {
  text-decoration: underline;
}
.category-main-link {
  background-color: white;
  max-width: 250px;
  margin: 0 auto;
}
.home-page {
  font-family: Arial, sans-serif;
  color: #fff;
  background-color: #00274d;
}

.hero {
  background: url("../assets/hero.png") no-repeat;
  background-position: right 55% bottom 50%;
  background-size: cover;
  height: 73.5vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 20px;
}

.hero-content {
  background: rgba(0, 0, 0, 0.5);
  border-radius: 10px;
  padding: 10px;
  margin-bottom: 390px;
}

.hero-content p {
  max-width: 600px;
  font-size: 18px;
  padding: 15px;
  border-radius: 8px;
  margin-top: 10px;
}
.news-section {
  padding: 40px;
  text-align: center;
}

.highlighted-section,
.gallery,
.cta {
  padding: 0 40px 40px;
  text-align: center;
}

.categories {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
  max-width: 850px;
  margin: 0 auto 50px;
}

.category-link {
  background: #ffcc00;
  color: #00274d;
  padding: 10px 15px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
  transition: 0.3s;
}

.category-link:hover {
  background: #e6b800;
}

.news-grid {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  justify-content: center;
}

.news-card {
  background: white;
  color: black;
  border-radius: 10px;
  padding: 15px;
  width: 100%;
  max-width: 300px;
  text-align: left;
}

.news-card img {
  width: 100%;
  border-radius: 10px;
}

.read-more {
  display: inline-block;
  margin-top: 10px;
  background: #ffcc00;
  color: #00274d;
  padding: 8px 12px;
  border-radius: 6px;
  text-decoration: none;
  font-weight: bold;
  transition: 0.3s;
}

.read-more:hover {
  background: #e6b800;
}

.cta {
  background: #ffd800;
  color: #00274d;
  padding: 50px 50px 70px;
}

.cta-button {
  background: #00274d;
  color: white;
  padding: 15px 25px;
  border-radius: 10px;
  text-decoration: none;
  font-size: 18px;
  font-weight: bold;
  transition: 0.3s;
}
.cta h2 {
  margin-bottom: 70px;
}

.cta-button:hover {
  background: #001a33;
}
</style>
