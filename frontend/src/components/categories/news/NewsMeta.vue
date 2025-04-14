<template>
  <div class="news-meta">
    <span class="news-author"> <i class="fas fa-user"></i> {{ author }} </span>
    <span class="news-date"> <i :class="icon"></i> {{ formattedDate }} </span>
    <span class="news-category">
      <i class="fa-solid fa-list"></i> {{ category }}
    </span>
  </div>
</template>

<script>
export default {
  props: {
    author: String,
    category: String,
    dateOfCreation: String,
    dateOfLastUpdate: String,
  },
  computed: {
    icon() {
      return new Date(this.dateOfCreation).getTime() ===
        new Date(this.dateOfLastUpdate).getTime()
        ? "fa fa-calendar"
        : "fa fa-edit";
    },
    formattedDate() {
      return new Date(this.dateOfCreation).toLocaleDateString("uk-UA", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "numeric",
        minute: "numeric",
      });
    },
  },
};
</script>

<style>
.news-meta {
  padding: 5px 0;
}
</style>
