<template>
  <hr />
  <div class="comments-section">
    <div class="display-text">
      <h2>Коментарі</h2>
      <button
        v-if="hasToken"
        @click="$emit('openPopup')"
        class="add-comment-button"
      >
        Додати коментар
      </button>
    </div>

    <div v-if="comments.length">
      <div v-for="comment in paginatedComments" :key="comment.id">
        <div class="comment">
          <div class="comment-header">
            <p class="comment-author">
              {{ comment.reader_first_name }} {{ comment.reader_last_name }}
            </p>
            <p class="comment-date">
              <i :class="getIcon(comment)"></i>
              {{ formatDate(comment.date_of_creation) }}
            </p>
          </div>

          <div class="rating">
            <span
              v-for="star in 5"
              :key="star"
              :class="{ filled: star <= comment.rating.length }"
            >
              ★
            </span>
          </div>

          <p class="comment-text">{{ comment.comment_text }}</p>

          <div class="container">
            <div class="comment-reactions" v-if="hasToken">
              <button
                @click="handleReactionChange(comment, 'Like')"
                :class="{ active: comment.user_reaction?.type === 'Like' }"
              >
                👌 {{ comment.likes_count }}
              </button>
              <button
                @click="handleReactionChange(comment, 'Dislike')"
                :class="{ active: comment.user_reaction?.type === 'Dislike' }"
              >
                🗿 {{ comment.dislikes_count }}
              </button>
            </div>

            <div v-else>
              <div class="comment-reactions">
                <div @click="handleReactionChange(comment, 'Like')" class="">
                  👌 {{ comment.likes_count }}
                </div>
                <div @click="handleReactionChange(comment, 'Dislike')">
                  🗿 {{ comment.dislikes_count }}
                </div>
              </div>
            </div>

            <div class="comment-actions" v-if="comment.is_creator">
              <button
                @click="$emit('editComment', comment.id)"
                class="edit-button"
              >
                ✏️ Редагувати
              </button>
              <button
                @click="$emit('delete-comment', comment.id)"
                class="delete-button"
              >
                🗑️ Видалити
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="pagination">
        <button @click="$emit('prevPage')" :disabled="currentPage === 1">
          &#9665;
        </button>
        <span>Сторінка {{ currentPage }} з {{ totalPages }}</span>
        <button
          @click="$emit('nextPage')"
          :disabled="currentPage === totalPages"
        >
          &#9655;
        </button>
      </div>
    </div>
    <div class="else" v-else>Коментарів поки немає.</div>
  </div>
</template>

<script>
export default {
  props: {
    comments: Array,
    currentPage: Number,
    totalPages: Number,
    paginatedComments: Array,
  },
  computed: {
    hasToken() {
      return !!this.$store.state.token;
    },
  },
  methods: {
    getIcon(comment) {
      return new Date(comment.date_of_creation).getTime() ===
        new Date(comment.date_of_last_update).getTime()
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
    handleReactionChange(comment, reactionType) {
      if (comment.user_reaction?.type === reactionType) {
        this.$emit("removeReaction", comment.user_reaction.id);
        console.log("Reaction ID to remove:", comment.user_reaction.id);
      } else {
        this.$emit(
          `${reactionType.toLowerCase()}Comment`,
          comment.id,
          reactionType
        );
      }
    },
  },
};
</script>

<style scoped>
.else {
  margin: 20px 0 0;
  text-align: center;
  font-size: 18px;
}
.container {
  display: flex;
  justify-content: space-between;
}
.comment-reactions {
  display: flex;
  gap: 10px;
  margin-top: 8px;
}

.comment-reactions button,
.comment-reactions div {
  background: #f4f4f4;
  border: 1px solid #ddd;
  padding: 6px 12px;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 5px;
}

.comment-reactions button.active {
  background: #ee7575;
  border-color: #e6b800;
  color: white;
  font-weight: bold;
}

.comment-reactions button:hover {
  background: #e0e0e0;
}

.comment-actions {
  display: flex;
  gap: 10px;
  margin-top: 8px;
}

.comment-actions .edit-button,
.comment-actions .delete-button {
  background: #fff;
  border: 1px solid #ccc;
  padding: 6px 12px;
  font-size: 14px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.comment-actions .edit-button {
  color: #007bff;
  border-color: #007bff;
}

.comment-actions .edit-button:hover {
  background: #007bff;
  color: #fff;
}

.comment-actions .delete-button {
  color: #dc3545;
  border-color: #dc3545;
}

.comment-actions .delete-button:hover {
  background: #dc3545;
  color: #fff;
}

.rating {
  margin-bottom: 10px;
}
.rating span {
  font-size: 24px;
  color: #ccc;
}

.rating span.filled {
  color: gold;
}

.comments-section {
  margin-top: 10px;
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
.display-text {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.add-comment-button {
  background: #ffcc00;
  color: #00274d;
  padding: 10px 15px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
  transition: 0.3s;
  font-size: 16px;
  cursor: pointer;
}
.active {
  color: #007bff;
}
.comment {
  border-top: 1px solid #ddd;
  padding: 10px 15px;
  margin-top: 20px;
  background: #f9f9f9;
  border-radius: 8px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  font-weight: bold;
}

.comment-text {
  margin-top: 5px;
  font-size: 16px;
  line-height: 1.4;
}

.comment-reactions {
  margin-top: 10px;
}

.like-button,
.dislike-button {
  margin-right: 10px;
  padding: 5px 10px;
  cursor: pointer;
}
</style>
