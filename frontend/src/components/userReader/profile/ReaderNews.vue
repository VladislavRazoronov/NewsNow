<template>
  <div class="page-container">
    <div v-if="loading" class="loading">Завантаження новин...</div>
    <div v-else>
      <div v-if="paginatedNews.length > 0" class="news-grid">
        <div
          v-for="newsItem in paginatedNews"
          :key="newsItem.id"
          class="news-card"
        >
          <img :src="getPhoto(newsItem)" alt="News Image" class="news-image" />
          <div class="news-info">
            <h3 class="news-title">{{ newsItem.title }}</h3>
            <div class="news-authors">
              <div class="author-info info-cont">
                <i class="fas fa-user"></i>
                <span>
                  {{ newsItem.author_first_name }}
                  {{ newsItem.author_last_name }}
                  {{ newsItem.author_patronymic }}
                </span>
              </div>
              <div class="news-author">
                <div class="category-info info-cont">
                  <i class="fa-solid fa-list"></i>
                  <span>{{ newsItem.category_name }}</span>
                </div>

                <div class="date-info info-cont">
                  <i class="fas fa-calendar-alt"></i>
                  <span>{{ formatDate(newsItem.date_of_saving) }}</span>
                </div>
              </div>
            </div>
            <router-link
              :to="`/news/${newsItem.news_id}`"
              class="read-more-btn"
            >
              Перейти до новини
            </router-link>
            <button class="delete-btn" @click="confirmDelete(newsItem.id)">
              Видалити
            </button>
          </div>
        </div>
      </div>
      <div v-else class="no-news">
        <img src="../../../assets/nothing.png" class="no-image" />
        <p>Ви ще не додали улюблені новини.</p>
        <router-link to="/categories">
          <i class="fas fa-plus-circle"></i> Додати новину
        </router-link>
      </div>
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
</template>

<script>
import { mapGetters } from "vuex";
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "FavoriteNewsList",
  data() {
    return {
      favoriteNews: [],
      loading: true,
      token: this.$store.state.token,
      page: 1,
      perPage: 6,
    };
  },
  computed: {
    ...mapGetters(["isAuthenticated"]),

    totalPages() {
      return Math.ceil(this.favoriteNews.length / this.perPage);
    },
    paginatedNews() {
      const start = (this.page - 1) * this.perPage;
      return this.favoriteNews.slice(start, start + this.perPage);
    },
  },
  async created() {
    if (this.isAuthenticated) {
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/news/reader_favorite_news/",
          {},
          {
            headers: {
              Authorization: `Token ${this.token}`,
            },
          }
        );

        if (response.status === 200) {
          this.favoriteNews = response.data.readers_favorite_news_list;
          console.log(this.favoriteNews);
        } else {
          console.error("Не вдалося отримати улюблені новини");
        }
      } catch (error) {
        console.error("Помилка завантаження новин:", error);
      } finally {
        this.loading = false;
      }
    } else {
      console.warn("Користувач не авторизований");
      this.loading = false;
    }
  },
  methods: {
    changePage(newPage) {
      if (newPage >= 1 && newPage <= this.totalPages) {
        this.page = newPage;
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

    confirmDelete(newsId) {
      Swal.fire({
        title: "Ви впевнені?",
        text: "Цю дію не можна скасувати!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Так, видалити",
        cancelButtonText: "Скасувати",
      }).then(async (result) => {
        if (result.isConfirmed) {
          await this.deleteFavoriteNews(newsId);
        }
      });
    },
    formatDate(dateOfCreation) {
      const createdDate = new Date(dateOfCreation);
      return createdDate.toLocaleDateString("uk-UA", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "numeric",
        minute: "numeric",
      });
    },
    async deleteFavoriteNews(newsId) {
      console.log(newsId);
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/news/delete_reader_favorite_news/",
          {
            favorite_news_to_delete_id: newsId,
          },
          {
            headers: {
              Authorization: `Token ${this.token}`,
            },
          }
        );

        if (response.status === 204) {
          this.favoriteNews = this.favoriteNews.filter(
            (newsItem) => newsItem.id !== newsId
          );
          Swal.fire({
            icon: "success",
            title: "Новину видалено зі збережених!",
            timer: 1500,
          });
        } else {
          Swal.fire({
            icon: "error",
            title: "Помилка!",
            text: "Не вдалося видалити новину.",
          });
        }
      } catch (error) {
        if (error.response) {
          if (error.response.status === 500) {
            Swal.fire({
              icon: "error",
              title: "Помилка сервера!",
              text: "Виникла помилка на сервері. Спробуйте ще раз пізніше.",
            });
          } else if (error.response.status === 404) {
            Swal.fire({
              icon: "error",
              title: "Новину не знайдено!",
              text: "Не вдалося знайти вказану новину для видалення.",
            });
          }
        } else if (error.request) {
          Swal.fire({
            icon: "error",
            title: "Помилка з'єднання!",
            text: "Не вдалося з'єднатися з сервером. Перевірте ваше підключення до Інтернету.",
          });
        } else {
          Swal.fire({
            icon: "error",
            title: "Невідома помилка!",
            text: "Сталася непередбачувана помилка. Спробуйте ще раз.",
          });
        }

        console.error("Помилка видалення новини:", error);
      }
    },
  },
};
</script>

<style scoped>
.no-news {
  font-size: 18px;
  text-align: center;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.no-news img {
  width: 350px;
}
.no-news a {
  text-decoration: none;
  font-size: 16px;
  display: flex;
  align-items: center;
  color: black;
  padding: 10px 15px;
  border-radius: 5px;
  transition: 0.3s ease-in-out;
}
.no-news a:hover {
  background-color: black;
  color: white;
}
.no-news a i {
  margin-right: 10px;
}
.info-cont {
  display: flex;
  align-items: center;
}
.info-cont i {
  margin-right: 8px;
}
.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-container div {
  margin: 0 auto;
}
.news-grid {
  max-width: 1100px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 50px;
  justify-items: center;
  margin: 0 auto;
}
@media (max-width: 1550px) {
  .news-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1200px) {
  .news-grid {
    grid-template-columns: repeat(1, 1fr);
  }
}
.news-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease-in-out;
  max-width: 350px;
}
.news-card:hover {
  transform: translateY(-5px);
}
.news-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
}
.news-info {
  padding: 15px;
}
.news-title {
  font-size: 1.2rem;
  margin: 0px;
  text-align: center;
  min-height: 70px;
}
.news-description {
  font-size: 0.9rem;
  color: #555;
}
.news-authors {
  font-size: 0.8rem;
  color: #777;
  margin-top: 10px;
}
.news-author {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}
.read-more-btn,
.delete-btn {
  display: block;
  text-align: center;
  padding: 8px 12px;
  margin-top: 10px;
  border-radius: 8px;
  text-decoration: none;
  font-size: 0.9rem;
}
.read-more-btn {
  background-color: #00274d;
  color: white;
}
.read-more-btn:hover {
  background-color: #0056b3;
}
.delete-btn {
  background: #e74c3c;
  color: white;
  margin: 10px auto 0;
  width: 100%;
  cursor: pointer;
}
.delete-btn:hover {
  background: #7f1509;
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
