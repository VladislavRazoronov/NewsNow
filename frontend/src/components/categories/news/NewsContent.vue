<template>
  <div class="news-content" v-html="formattedText"></div>
</template>

<script>
export default {
  props: {
    text: String,
  },
  computed: {
    formattedText() {
      return this.text
        ? this.text
            .split("\n")
            .map((paragraph) => `<p>${paragraph}</p>`)
            .join("")
        : "";
    },
  },
};
</script>
