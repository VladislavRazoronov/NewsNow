<template>
  <div class="add-news-page">
    <h2>Додати новину</h2>
    <form @submit.prevent="submitNews">
      <div class="form-group">
        <label for="category">Категорія:</label>
        <select v-model="news.category_id" required>
          <option
            v-for="category in categories"
            :key="category.id"
            :value="category.id"
          >
            {{ category.category_name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="title">Заголовок:</label>
        <input type="text" id="title" v-model="news.title" required />
      </div>

      <div class="form-group">
        <label for="image">Зображення:</label>
        <input type="file" id="image" @change="handleFileUpload" required />
        <div v-if="imagePreview" class="image-preview">
          <img :src="imagePreview" alt="Передперегляд зображення" />
        </div>
      </div>

      <div class="form-group">
        <label for="text">Текст новини:</label>
        <textarea id="text" v-model="news.text" required></textarea>
      </div>

      <button type="submit">Додати новину</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      categories: [],
      news: {
        category_id: "",
        title: "",
        image: null,
        text: "",
      },
      imagePreview: "",
    };
  },
  mounted() {
    this.fetchCategories();
    this.token = this.$store.state.token;
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
        }
      } catch (error) {
        console.error("Помилка завантаження категорій:", error);
      }
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      const allowedTypes = [
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp",
      ];
      if (!allowedTypes.includes(file.type)) {
        Swal.fire({
          icon: "error",
          title: "Непідтримуваний формат файлу",
          text: "Будь ласка, виберіть зображення у форматі JPEG, PNG, GIF або WebP.",
        });
        return;
      }

      this.imagePreview = URL.createObjectURL(file);
      this.news.image = file;

      console.log("Файл вибрано:", file);
      console.log("Посилання на прев’ю:", this.imagePreview);
    },
    async submitNews() {
      const trimmedTitle = this.news.title.trim();
      const trimmedText = this.news.text.trim();

      if (!trimmedTitle || !trimmedText) {
        Swal.fire({
          icon: "error",
          title: "Помилка",
          text: "Заголовок та текст новини не можуть бути порожніми або містити лише пробіли.",
        });
        return;
      }

      try {
        const formData = new FormData();
        formData.append("category_id", this.news.category_id);
        formData.append("title", trimmedTitle);
        formData.append("image", this.news.image);
        formData.append("text", trimmedText);

        const response = await axios.post(
          "http://127.0.0.1:8000/news/add_news/",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
              Authorization: `Token ${this.token}`,
            },
          }
        );

        if (response.status === 201) {
          Swal.fire({
            icon: "success",
            title: "Новину додано успішно",
          }).then(() => {
            this.$router.push("/profile-journalist/my-news");
          });
        } else {
          Swal.fire({
            icon: "error",
            title: "Помилка при додаванні новини",
          });
        }
      } catch (error) {
        console.error("Помилка при додаванні новини:", error);
      }
    },
  },
};
</script>

<style scoped>
.image-preview {
  margin: 20px auto;
  display: flex;
  justify-content: center;
}
.image-preview img {
  max-width: 300px;
  margin-top: 10px;
  display: block;
  border-radius: 5px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.add-news-page {
  max-width: 600px;
  margin: auto;
  padding: 20px;
}
.form-group {
  margin-bottom: 15px;
}
label {
  display: block;
  font-weight: bold;
}
input,
select,
textarea {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 4px;
}
button:hover {
  background-color: #218838;
}
</style>
