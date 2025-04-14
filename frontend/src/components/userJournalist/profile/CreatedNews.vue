<template>
  <div class="page-container">
    <div v-if="loading" class="loading">Завантаження новин...</div>
    <div v-else>
      <div class="container-news" v-if="paginatedNews.length > 0">
        <div
          v-for="newsItem in paginatedNews"
          :key="newsItem.id"
          class="news-card"
        >
          <div class="image-container">
            <img
              :src="getPhoto(newsItem)"
              alt="news Image"
              class="news-image"
            />
            <button @click="confirmDelete(newsItem.id)" class="delete-news-btn">
              <i class="fa fa-trash"></i>
            </button>
          </div>
          <div class="news-info">
            <h3 class="news-title">{{ newsItem.title }}</h3>
            <div class="news-details">
              <div class="detail-item">
                <i
                  :class="
                    getIcon(
                      newsItem.date_of_creation,
                      newsItem.date_of_last_update
                    )
                  "
                ></i>
                {{
                  formatDate(
                    newsItem.date_of_creation,
                    newsItem.date_of_last_update
                  )
                }}
              </div>

              <br />
              <div class="detail-item">
                <i class="fa-solid fa-list"></i> {{ newsItem.category_name }}
              </div>
            </div>
            <router-link :to="`/news/${newsItem.id}`" class="start-news-btn">
              Детальніше
            </router-link>
            <router-link
              :to="`/profile-journalist/edit-news/${newsItem.id}`"
              class="edit-news-btn"
            >
              Редагувати
            </router-link>
          </div>
        </div>
      </div>

      <div v-else class="no-news">
        <img src="../../../assets/nothing.png" class="no-image" />
        <p>Немає створених новин.</p>
        <router-link to="/profile-journalist/add-news">
          <i class="fa-solid fa-square-plus"></i> Додати новину
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
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "AuthorsNews",
  data() {
    return {
      newsList: [],
      loading: true,
      page: 1,
      perPage: 6,
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.newsList.length / this.perPage);
    },
    paginatedNews() {
      const start = (this.page - 1) * this.perPage;
      return this.newsList.slice(start, start + this.perPage);
    },
  },
  created() {
    this.fetchNews();
  },
  methods: {
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

    getPhoto(news) {
      try {
        const photoPath = news.image.split("media/images/news_images/")[1];
        if (!photoPath) throw new Error("Invalid image path");

        const decodedFileName = decodeURIComponent(photoPath.split("/").pop());

        return require(`@/../../backend/media/images/news_images/${decodedFileName}`);
      } catch (error) {
        console.error("Error loading photo:", error);
        return "";
      }
    },
    changePage(newPage) {
      if (newPage >= 1 && newPage <= this.totalPages) {
        this.page = newPage;
      }
    },
    async fetchNews() {
      this.loading = true;
      try {
        const token = this.$store.state.token;
        const response = await axios.post(
          "http://127.0.0.1:8000/news/authors_news/",
          {},
          {
            headers: { Authorization: `Token ${token}` },
          }
        );
        this.newsList = response.data.authors_news_list;
        console.log(this.newsList);
      } catch (error) {
        console.error("Помилка завантаження новин:", error);
      } finally {
        this.loading = false;
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
          await this.deleteNews(newsId);
        }
      });
    },
    async deleteNews(newsId) {
      const token = this.$store.state.token;
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/news/delete_news/",
          { news_to_delete_id: newsId },
          {
            headers: { Authorization: `Token ${token}` },
          }
        );

        if (response.status === 204) {
          this.fetchNews();
          Swal.fire({
            icon: "success",
            title: "Новину успішно видалено!",
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
        console.error("Помилка при видаленні новини:", error);
        Swal.fire({
          icon: "error",
          title: "Сталася помилка!",
          text: "Спробуйте ще раз.",
        });
      }
    },
  },
};
</script>

<style scoped>
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
.image-container {
  position: relative;
  display: flex;
  justify-content: center;
}

.delete-news-btn {
  background-color: transparent;
  border: none;
  cursor: pointer;
  font-size: 20px;
  color: #e74c3c;
  position: absolute;
  top: 10px;
  right: 10px;
}

.delete-news-btn:hover {
  transform: scale(1.1);
}

.delete-news-btn i {
  font-size: 24px;
}

.news-card {
  position: relative;
  border: 1px solid #ddd;
  border-radius: 10px;
  overflow: hidden;
}

.news-info {
  padding: 20px;
}

.container-news {
  max-width: 1100px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 50px;
  justify-items: center;
}

@media (max-width: 1550px) {
  .container-news {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1200px) {
  .container-news {
    grid-template-columns: repeat(1, 1fr);
  }
}

.plus-icon {
  font-size: 30px;
  color: #2ecc71;
}

.add-news-content {
  font-size: 18px;
  color: #ffcc00;
}

.page-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: #f8f9fa;
  padding: 10px 0;
}

.page-container div {
  margin: 0 auto;
}

.news-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease;
  text-align: center;
  padding-bottom: 10px;
  width: 320px;
}

.news-card:hover {
  transform: translateY(-5px);
}

.news-image {
  width: 320px;
  height: 180px;
  object-fit: cover;
}

.news-info {
  padding: 15px 20px;
}

.news-title {
  font-size: 20px;
  font-weight: bold;
  margin: 10px;
  min-height: 70px;
}

.news-details {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  font-size: 14px;
  color: #666;
  padding: 5px 0;
}

.detail-item {
  text-align: left;
  gap: 5px;
}

.news-details .detail-item:nth-of-type(2) {
  text-align: left;
}

.start-news-btn {
  display: block;
  margin: 15px auto 0;
  padding: 10px 20px;
  background-color: #00274d;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  transition: background 0.3s ease;
}

.start-news-btn:hover {
  background-color: #0056b3;
}

.add-news-card {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 320px;
  height: 180px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  font-size: 20px;
  font-weight: bold;
  color: #007bff;
  border: 2px dashed #00274d;
  transition: background 0.3s ease, transform 0.3s ease;
}

.add-news-card:hover {
  background: #e6f0ff;
  transform: translateY(-5px);
}

.add-news-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.plus-icon {
  font-size: 40px;
  font-weight: bold;
  margin-bottom: 5px;
  color: #00274d;
}
.edit-news-btn {
  display: block;
  margin: 10px auto;
  padding: 8px 15px;
  background-color: #28a745;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  transition: background 0.3s ease;
}

.edit-news-btn:hover {
  background-color: #218838;
}
.delete-news-btn {
  display: block;
  margin: 10px auto;
  padding: 8px 15px;
  background-color: #dc3545;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: background 0.3s ease;
}

.delete-news-btn:hover {
  background-color: #c82333;
}
</style>
