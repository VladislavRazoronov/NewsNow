<template>
  <div class="news-article">
    <div class="news-buttons">
      <button @click="$router.go(-1)" class="back-button">&larr; Назад</button>
      <button v-if="isReader" @click="saveNews" class="save-button">
        Зберегти новину
      </button>
    </div>

    <div v-if="newsItem">
      <h1 class="news-title">{{ newsItem.title }}</h1>

      <hr />

      <NewsMeta
        :author="newsItem.author_first_name + ' ' + newsItem.author_last_name"
        :category="newsItem.category_name"
        :dateOfCreation="newsItem.date_of_creation"
        :dateOfLastUpdate="newsItem.date_of_last_update"
      />

      <NewsImage :imageUrl="getPhoto(newsItem)" />
      <NewsContent :text="newsItem.text" />

      <CommentsSection
        :comments="newsItem.comments"
        :currentPage="currentPage"
        :totalPages="totalPages"
        :paginatedComments="paginatedComments"
        @prevPage="prevPage"
        @nextPage="nextPage"
        @openPopup="openPopup"
        @editComment="editComment"
        @deleteComment="deleteComment"
        @likeComment="addOrUpdateReaction"
        @dislikeComment="addOrUpdateReaction"
        @reaction-changed="handleReactionChange"
        @removeReaction="deleteReaction"
        @comment-updated="handleCommentUpdated"
      />

      <EditComment
        v-if="editingCommentId !== null"
        :commentId="editingCommentId"
        :fetch-news-details="fetchNewsDetails"
        @close="handleCloseEditComment"
      />

      <AddCommentForm
        v-if="showPopup"
        :showPopup="showPopup"
        :newsId="newsId"
        @closePopup="closePopup"
        @submit-comment="submitComment"
      />
    </div>

    <div v-else>
      <p>Новина не знайдена.</p>
    </div>
  </div>
</template>

<script>
import NewsMeta from "./news/NewsMeta.vue";
import NewsImage from "./news/NewsImage.vue";
import NewsContent from "./news/NewsContent.vue";
import CommentsSection from "./news/CommentsSection.vue";
import AddCommentForm from "./news/AddCommentForm.vue";
import EditComment from "./news/EditComment.vue";
import axios from "axios";
import Swal from "sweetalert2";

export default {
  components: {
    NewsMeta,
    NewsImage,
    NewsContent,
    CommentsSection,
    AddCommentForm,
    EditComment,
  },
  props: {
    comment: Object,
  },

  data() {
    return {
      newsItem: null,
      newsId: this.$route.params.id,
      token: this.$store.state.token || null,
      showPopup: false,
      currentPage: 1,
      commentsPerPage: 5,
      user_reaction: null,
      editingCommentId: null,
    };
  },
  mounted() {
    this.fetchNewsDetails();
  },
  computed: {
    isReader() {
      return this.$store.getters.account_type === "Читач";
    },
    totalPages() {
      return Math.ceil(
        (this.newsItem?.comments.length || 0) / this.commentsPerPage
      );
    },
    sortedComments() {
      return (
        this.newsItem?.comments
          .slice()
          .sort(
            (a, b) =>
              new Date(b.date_of_creation) - new Date(a.date_of_creation)
          ) || []
      );
    },
    paginatedComments() {
      const start = (this.currentPage - 1) * this.commentsPerPage;
      return this.sortedComments.slice(start, start + this.commentsPerPage);
    },
    formattedText() {
      return this.newsItem
        ? this.newsItem.text
            .split("\n")
            .map((paragraph) => `<p>${paragraph}</p>`)
            .join("")
        : "";
    },
  },
  methods: {
    handleCloseEditComment() {
      this.editingCommentId = null;
      this.fetchNewsDetails();
    },

    editComment(commentId) {
      this.editingCommentId = commentId;
    },
    async submitComment() {
      await this.fetchNewsDetails();
    },

    openPopup() {
      this.showPopup = true;
    },

    closePopup() {
      this.showPopup = false;
    },
    prevPage() {
      if (this.currentPage > 1) this.currentPage--;
    },
    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage++;
    },
    handleCommentUpdated(updatedComment) {
      const index = this.newsItem.comments.findIndex(
        (comment) => comment.id === updatedComment.id
      );
      if (index !== -1) {
        this.$set(this.newsItem.comments, index, updatedComment);
      }
    },
    async handleReactionChange(comment, reactionType) {
      if (
        comment.user_reaction &&
        comment.user_reaction.type === reactionType
      ) {
        this.$set(comment, "user_reaction", null);
        this.updateLocalReaction(comment.id, null);
      } else {
        this.$set(comment, "user_reaction", { type: reactionType });
        this.updateLocalReaction(comment.id, reactionType);
      }

      const updatedComment = { ...comment };
      this.handleCommentUpdated(updatedComment);
    },
    async saveNews() {
      try {
        const headers = this.token
          ? { Authorization: `Token ${this.token}` }
          : {};
        const response = await axios.post(
          "http://127.0.0.1:8000/news/add_reader_favorite_news/",
          { news_id: this.newsId },
          { headers }
        );

        if (response.status === 201) {
          Swal.fire({
            title: "Успішно!",
            text: "Новину успішно збережено.",
            icon: "success",
            confirmButtonText: "OK",
          });
        } else {
          throw new Error("Не вдалося зберегти новину");
        }
      } catch (error) {
        if (error.response && error.response.status === 400) {
          const serverMessage = error.response.data?.Message?.trim();
          let errorMessage = "Не вдалося зберегти новину.";

          if (serverMessage === "this news is already in favorites.") {
            errorMessage = "Ця новина вже є у вибраному.";
          }

          console.log(serverMessage); // Перевіряємо, що приходить у помилці

          Swal.fire({
            title: "Помилка",
            text: errorMessage,
            icon: "error",
            confirmButtonText: "OK",
          });
        } else {
          console.error("Помилка збереження новини:", error);

          Swal.fire({
            title: "Помилка",
            text: "Не вдалося зберегти новину.",
            icon: "error",
            confirmButtonText: "OK",
          });
        }
      }
    },
    async deleteComment(commentId) {
      const result = await Swal.fire({
        title: "Ви впевнені?",
        text: "Цей коментар буде видалено безповоротно!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Так, видалити!",
        cancelButtonText: "Скасувати",
      });

      if (!result.isConfirmed) return;

      try {
        const headers = this.token
          ? { Authorization: `Token ${this.token}` }
          : {};
        await axios.post(
          "http://127.0.0.1:8000/news/delete_comment/",
          { comment_to_delete_id: commentId },
          { headers }
        );

        this.newsItem.comments = this.newsItem.comments.filter(
          (comment) => comment.id !== commentId
        );

        Swal.fire({
          title: "Видалено!",
          text: "Коментар успішно видалено.",
          icon: "success",
          timer: 2000,
          showConfirmButton: false,
        });
      } catch (error) {
        console.error("Помилка видалення коментаря:", error);

        Swal.fire({
          title: "Помилка",
          text: "Не вдалося видалити коментар.",
          icon: "error",
          confirmButtonText: "OK",
        });
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

    updateLocalReaction(commentId, reactionType) {
      const comment = this.newsItem.comments.find((c) => c.id === commentId);
      if (comment) {
        if (comment.user_reaction?.type === "Like") {
          comment.likes_count--;
        } else if (comment.user_reaction?.type === "Dislike") {
          comment.dislikes_count--;
        }

        comment.user_reaction = { type: reactionType };

        if (reactionType === "Like") {
          comment.likes_count++;
        } else if (reactionType === "Dislike") {
          comment.dislikes_count++;
        }
      }
    },
    async fetchNewsDetails() {
      try {
        const headers = this.token
          ? { Authorization: `Token ${this.token}` }
          : {};
        const response = await axios.post(
          `http://127.0.0.1:8000/news/news_comments_and_reactions/`,
          { news_id: this.newsId },
          { headers }
        );

        if (response.status === 200 && response.data.news_info) {
          this.newsItem = response.data.news_info[0];
          this.newsItem.comments =
            response.data.news_comments_and_reactions || [];
          console.log(this.newsItem);
        } else {
          console.warn("Новина не знайдена.");
        }
      } catch (error) {
        console.error("Помилка завантаження новини:", error);
      }
    },

    getIcon(dateOfCreation, dateOfLastUpdate) {
      return new Date(dateOfCreation).getTime() ===
        new Date(dateOfLastUpdate).getTime()
        ? "fa fa-calendar"
        : "fa fa-edit";
    },

    formatDate(date) {
      return new Date(date).toLocaleDateString("uk-UA", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "numeric",
        minute: "numeric",
      });
    },

    compareDates(dateOfCreation, dateOfLastUpdate) {
      const createdAt = new Date(dateOfCreation).toISOString().slice(0, 19);
      const updatedAt = new Date(dateOfLastUpdate).toISOString().slice(0, 19);

      return createdAt === updatedAt
        ? this.formatDate(dateOfCreation)
        : `Ред. ${this.formatDate(dateOfLastUpdate)}`;
    },

    async toggleReaction(commentId, reactionType) {
      const userReaction = this.getUserReaction(commentId);

      if (userReaction === reactionType) {
        await this.deleteReaction(commentId);
      } else {
        await this.addOrUpdateReaction(commentId, reactionType);
      }

      await this.fetchNewsDetails();
    },
    async likeComment(commentId) {
      const userReaction = this.getUserReaction(commentId);

      if (userReaction === "Like") {
        console.log("You've already liked this comment");
        return;
      } else if (userReaction === "Dislike") {
        await this.deleteReaction(commentId);
      }

      console.log(`Sending Like for comment ${commentId}`);
      await this.addOrUpdateReaction(commentId, "Like");
    },
    async dislikeComment(commentId) {
      const userReaction = this.getUserReaction(commentId);

      if (userReaction === "Dislike") {
        console.log("You've already disliked this comment");
        return;
      } else if (userReaction === "Like") {
        await this.deleteReaction(commentId);
      }

      console.log(`Sending Dislike for comment ${commentId}`);
      await this.addOrUpdateReaction(commentId, "Dislike");
    },
    getUserReaction(commentId) {
      const comment = this.newsItem.comments.find((c) => c.id === commentId);
      if (!comment || !comment.user_reaction) {
        console.log("No reaction for this comment");
        return null;
      }
      console.log("User Reaction:", comment.user_reaction);
      return comment.user_reaction;
    },
    async addOrUpdateReaction(commentId, reactionType) {
      if (!reactionType) {
        console.error("reactionType is undefined!");
        return;
      }

      try {
        const headers = this.token
          ? { Authorization: `Token ${this.token}` }
          : {};

        const formData = {
          comment_id: commentId,
          reaction: reactionType,
        };

        const response = await axios.post(
          "http://127.0.0.1:8000/news/add_or_update_reaction/",
          formData,
          { headers }
        );

        if (response.status === 200) {
          console.log(`Reaction updated for comment ${commentId}`);
          this.updateLocalReaction(commentId, reactionType);
          await this.fetchNewsDetails();
        }
      } catch (error) {
        console.error(`Error updating reaction:`, error);
      }
    },

    async deleteReaction(userReactionId) {
      try {
        const reactionToDelete = this.newsItem.comments
          .map((comment) => {
            console.log("Comment user_reaction:", comment.user_reaction);
            return comment.user_reaction;
          })
          .find((reaction) => reaction && reaction.id === userReactionId);

        console.log("Reaction to delete:", reactionToDelete);
        console.log(userReactionId);
        const headers = this.token
          ? { Authorization: `Token ${this.token}` }
          : {};
        await axios.post(
          "http://127.0.0.1:8000/news/delete_reaction/",
          { reaction_to_delete_id: reactionToDelete.id },
          { headers }
        );
        await this.fetchNewsDetails();

        console.log(
          `Reaction removed for comment ${this.reaction_to_delete_id}`
        );
      } catch (error) {
        console.error("Error removing reaction:", error);
      }
    },
  },
};
</script>

<style scoped>
.active {
  color: #007bff;
}

.news-article {
  max-width: 800px;
  margin: 50px auto;
  font-family: Arial, sans-serif;
}

.news-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.news-buttons button {
  display: inline-block;
  margin-bottom: 15px;
  padding: 8px 15px;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: 0.3s ease-in-out;
}

.back-button {
  color: white;
  background-color: #007bff;
  border: none;
}

.back-button:hover {
  background-color: #0056b3;
}

.save-button {
  color: #00274d;
  background-color: #ffcc00;
  border: 2px solid #00274d;
}

.save-button:hover {
  background-color: #0159b1;
  color: #ffcc00;
  border: 2px solid #ffcc00;
}

.news-title {
  font-size: 28px;
  line-height: 1.3;
  font-weight: bold;
  margin-bottom: 10px;
  text-align: justify;
}

.news-meta {
  color: #777;
  font-size: 14px;
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
}

.news-meta span {
  margin-right: 15px;
}

.news-image {
  width: 100%;
  height: auto;
  border-radius: 10px;
  margin-bottom: 20px;
}

.news-content {
  width: 800px;
  font-size: 18px;
  line-height: 1.6;
  text-align: justify;
  padding-bottom: 10px;
}
</style>
