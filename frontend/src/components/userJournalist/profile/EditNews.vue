<template>
  <main class="edit-news-form">
    <h2>Редагувати новину</h2>
    <form @submit.prevent="submitNews">
      <label for="title">Заголовок новини:</label>
      <input v-model="news.title" type="text" id="title" required />

      <label for="category_name">Категорія:</label>
      <select v-model="news.category_name" id="category_name" required>
        <option
          v-for="category in categories"
          :key="category.id"
          :value="category.category_name"
        >
          {{ category.category_name }}
        </option>
      </select>

      <label for="text">Текст новини:</label>
      <textarea v-model="news.text" id="text" required rows="6"></textarea>

      <label for="image">Зображення новини:</label>
      <input
        type="file"
        id="image"
        accept="image/png, image/jpeg, image/gif"
        @change="handleFileUpload"
      />

      <img
        :src="imagePreview || getPhoto(news)"
        alt="Попередній перегляд"
        class="preview-image"
      />

      <button type="submit">Зберегти зміни</button>
    </form>
  </main>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      news: {
        id: "",
        title: "",
        category_name: "",
        text: "",
        image: "",
      },
      categories: [],
      imagePreview: "",
      token: "",
      news_id: null,
    };
  },
  computed: {
    ...mapGetters(["isAuthenticated"]),
  },
  async mounted() {
    this.token = this.$store.state.token;
    this.news_id = this.$route.params.id;
    await this.fetchCategories();
    if (!this.news_id) return;
    await this.fetchNewsData();
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
          console.log(this.categories);
        } else {
          console.warn("Категорії новин не знайдено.");
        }
      } catch (error) {
        console.error("Помилка завантаження категорій:", error);
      }
    },
    async fetchNewsData() {
      try {
        const response = await axios.post(
          `http://127.0.0.1:8000/news/news_info/`,
          { news_id: this.news_id },
          { headers: { Authorization: `Token ${this.token}` } }
        );
        if (response.data) {
          this.news = response.data.news_info[0];

          this.news.title = this.news.title || "";
          this.news.category_name = this.news.category_name || "";
          this.news.text = this.news.text || "";

          this.news.image = this.news.image || "";
        }
      } catch (error) {
        Swal.fire({
          icon: "error",
          title: "Помилка",
          text: "Не вдалося завантажити дані новини.",
        });
      }
    },

    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      const allowedTypes = ["image/jpeg", "image/png", "image/gif"];
      const maxSize = 2 * 1024 * 1024;

      if (!allowedTypes.includes(file.type)) {
        Swal.fire({
          icon: "error",
          title: "Неправильний формат файлу",
          text: "Будь ласка, завантажте зображення у форматі JPG, PNG або GIF.",
        });
        return;
      }

      if (file.size > maxSize) {
        Swal.fire({
          icon: "error",
          title: "Файл завеликий",
          text: "Максимальний розмір файлу – 2MB.",
        });
        return;
      }
      this.imagePreview = URL.createObjectURL(file);
      this.news.image = file;
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

      const formData = new FormData();
      formData.append("news_to_update_id", this.news.id);
      formData.append("new_title", trimmedTitle);
      formData.append(
        "new_category_id",
        this.categories.find(
          (category) => category.category_name === this.news.category_name
        )?.id || ""
      );
      formData.append("new_text", trimmedText);
      formData.append("new_image", this.news.image);

      console.log("Відправлені дані:");
      for (let [key, value] of formData.entries()) {
        console.log(`${key}:`, value);
      }

      try {
        await axios.post("http://127.0.0.1:8000/news/update_news/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Token ${this.token}`,
          },
        });
        Swal.fire({
          icon: "success",
          title: "Новину успішно відредаговано!",
          confirmButtonText: "OK",
        }).then(() => {
          this.$router.push(`/news/${this.news.id}`);
        });
      } catch (error) {
        Swal.fire({
          icon: "error",
          title: "Помилка",
          text: "Не вдалося відредагувати новину.",
        });
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
  },
};
</script>

<style scoped>
.preview-image {
  max-width: 400px;
  margin: 10px auto 30px;
  display: block;
  border-radius: 5px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.edit-course-form {
  box-sizing: border-box;
  width: 800px;
  margin: 0 auto;
  padding: 30px;
  height: 80vh;
  overflow-y: auto;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: bold;
  margin-top: 10px;
  color: #555;
}

input,
textarea,
select {
  padding: 12px;
  margin-top: 8px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
  transition: border-color 0.3s ease-in-out;
}

input:focus,
textarea:focus,
select:focus {
  border-color: #007bff;
  outline: none;
}

textarea {
  resize: vertical;
  min-height: 100px;
  height: 150px;
}

button {
  padding: 12px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
  font-size: 16px;
}

button:hover {
  background-color: #0056b3;
}

button:focus {
  outline: none;
}
</style>
