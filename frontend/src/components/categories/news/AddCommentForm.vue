<template>
  <div class="popup-overlay" v-if="showPopup">
    <div class="popup">
      <h3>Додати коментар</h3>

      <div class="rating">
        <span
          v-for="star in 5"
          :key="star"
          class="star"
          :class="{ active: star <= rating.length }"
          @click="setRating(star)"
        >
          ★
        </span>
      </div>

      <textarea v-model="commentText" placeholder="Ваш коментар"></textarea>
      <div class="button-container">
        <button @click="submitComment">Зберегти</button>
        <button @click="closePopup">Закрити</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  props: {
    showPopup: Boolean,
    newsId: Number,
  },
  data() {
    return {
      commentText: "",
      rating: "",
      token: this.$store.state.token || null,
    };
  },
  methods: {
    closePopup() {
      this.$emit("close-popup");
    },

    setRating(star) {
      this.rating = "★".repeat(star);
    },

    async submitComment() {
      if (!this.commentText.trim()) {
        Swal.fire("Помилка!", "Коментар не може бути порожнім!", "error");
        return;
      }

      if (!this.rating) {
        Swal.fire("Помилка!", "Будь ласка, виберіть рейтинг!", "error");
        return;
      }

      const commentData = {
        news_id: this.newsId,
        comment_text: this.commentText,
        rating: this.rating,
      };

      try {
        const headers = this.token
          ? { Authorization: `Token ${this.token}` }
          : {};

        const response = await axios.post(
          "http://127.0.0.1:8000/news/add_comment/",
          commentData,
          { headers }
        );

        if (response.status === 201) {
          Swal.fire("Готово!", "Коментар додано успішно! 🎉", "success");

          this.$emit("submit-comment", this.commentText);
          this.closePopup();
          this.commentText = "";
          this.rating = "";
        } else {
          Swal.fire("Помилка!", "Не вдалося додати коментар.", "error");
        }
      } catch (error) {
        console.error("Помилка при додаванні коментаря:", error);

        Swal.fire({
          title: "Помилка!",
          text: error.response?.data?.message || "Щось пішло не так.",
          icon: "error",
        });
      }
    },
  },
};
</script>

<style scoped>
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 400px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease;
  box-sizing: border-box;
}

h3 {
  font-size: 24px;
  margin-bottom: 15px;
  text-align: center;
}

textarea {
  box-sizing: border-box;
  width: 100%;
  height: 100px;
  padding: 10px;
  margin-bottom: 20px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 14px;
  resize: none;
  outline: none;
  transition: border-color 0.3s ease;
}

textarea:focus {
  border-color: #00274d;
}

.button-container {
  display: flex;
  justify-content: space-between;
}

button {
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  background-color: #00274d;
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: rgb(68, 127, 156);
}

button:focus {
  outline: none;
}

.rating {
  margin-bottom: 10px;
  text-align: center;
}

.star {
  font-size: 24px;
  cursor: pointer;
  color: #ccc;
  transition: color 0.3s ease;
}

.star.active {
  color: gold;
}

.star:hover {
  color: #f1c40f;
}
</style>
