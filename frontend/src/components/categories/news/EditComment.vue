<template>
  <div class="modal-overlay">
    <div class="modal">
      <h2>Редагування коментаря</h2>

      <div v-if="loading">Завантаження...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else>
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

        <textarea v-model="commentText" rows="4"></textarea>
      </div>

      <div class="button-container">
        <button @click="submitEdit">Зберегти</button>
        <button @click="close">Закрити</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  props: {
    commentId: Number,
  },
  data() {
    return {
      commentText: "",
      rating: "",
      loading: false,
      error: null,
      token: this.$store.state.token || null,
    };
  },

  methods: {
    async fetchComment() {
      this.loading = true;
      this.error = null;

      if (!this.token) {
        this.error = "Користувач не авторизований";
        this.loading = false;
        return;
      }

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/news/comment_info/",
          { comment_id: this.commentId },
          {
            headers: {
              Authorization: `Token ${this.token}`,
            },
          }
        );

        this.commentText = response.data.comment_info[0].comment_text;
        this.rating = response.data.comment_info[0].rating || "";
        console.log(this.commentText);
      } catch (err) {
        this.error =
          err.response?.data?.message || "Помилка при отриманні коментаря";
      } finally {
        this.loading = false;
      }
    },
    setRating(star) {
      this.rating = "★".repeat(star);
    },
    async submitEdit() {
      if (!this.commentText.trim()) {
        Swal.fire("Помилка!", "Коментар не може бути порожнім!", "error");
        return;
      }

      try {
        await axios.post(
          "http://127.0.0.1:8000/news/update_comment/",
          {
            comment_id: this.commentId,
            new_comment_text: this.commentText,
            new_rating: this.rating,
          },
          {
            headers: { Authorization: `Token ${this.token}` },
          }
        );

        const updatedComment = {
          id: this.commentId,
          commentText: this.commentText,
          rating: this.rating,
        };

        this.$emit("comment-updated", updatedComment);
        this.$emit("close");

        await Swal.fire({
          title: "Готово!",
          text: "Коментар оновлено успішно!",
          icon: "success",
          confirmButtonText: "Ok",
        });

        this.close();
      } catch (error) {
        Swal.fire({
          title: "Помилка!",
          text: error.response?.data?.message || "Не вдалося оновити коментар.",
          icon: "error",
        });
      }
    },
    close() {
      this.$emit("close");
    },
  },
  mounted() {
    this.fetchComment();
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  min-width: 300px;
  text-align: center;
}

textarea {
  width: 100%;
  padding: 5px;
  margin-top: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.close-button {
  margin-top: 10px;
  padding: 5px 10px;
  background: red;
  color: white;
  border: none;
  cursor: pointer;
}

.error {
  color: red;
  font-weight: bold;
}
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
