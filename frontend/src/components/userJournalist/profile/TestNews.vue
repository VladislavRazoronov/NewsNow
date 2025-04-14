<template>
  <div>
    <button @click="updateNews">Update News</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newsToUpdateId: this.$route.params.id,
      newCategory: "New Category",
      newTitle: "Updated Title",
      newText: "Updated text here.",
      newImage: null,
    };
  },
  methods: {
    async updateNews() {
      const formData = new FormData();
      formData.append("news_to_update_id", this.newsToUpdateId);
      formData.append("new_category", this.newCategory);
      formData.append("new_title", this.newTitle);
      formData.append("new_text", this.newText);

      if (this.newImage) {
        formData.append("new_image", this.newImage);
      }

      try {
        const response = await this.$axios.post(
          "http://127.0.0.1:8000/news/update_news/",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        console.log("Response:", response);
      } catch (error) {
        console.error("Error updating news:", error);
      }
    },
  },
};
</script>
