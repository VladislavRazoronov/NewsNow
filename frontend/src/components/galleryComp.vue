<template>
  <div class="gallery">
    <h2>Фотографії Стрия</h2>
    <div class="gallery-grid">
      <div
        v-for="(image, index) in galleryImages"
        :key="index"
        :class="['gallery-item', image.className]"
        @click="openModal(image.src)"
      >
        <img :src="image.src" :alt="'Image ' + index" />
      </div>
    </div>

    <div v-if="isModalOpen" class="modal" @click="closeModal">
      <img :src="modalImage" class="modal-image" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      galleryImages: [
        { src: require("@/assets/im1.png"), className: "im1" },
        { src: require("@/assets/im2.png"), className: "im2" },
        { src: require("@/assets/im3.png"), className: "im3" },
        { src: require("@/assets/im4.png"), className: "im4" },
        { src: require("@/assets/im5.png"), className: "im5" },
        { src: require("@/assets/im6.png"), className: "im6" },
        { src: require("@/assets/im7.png"), className: "im7" },
      ],
      isModalOpen: false,
      modalImage: null,
    };
  },
  methods: {
    openModal(imageSrc) {
      this.modalImage = imageSrc;
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
    },
  },
};
</script>

<style scoped>
.gallery {
  text-align: center;
  width: 1100px;
  margin: 0 auto;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(5, 250px);
  gap: 8px;
  grid-template-areas:
    "im1 im2 im2"
    "im1 im3 im4"
    "im1 im3 im5"
    "im6 im6 im5"
    "im7 im7 im7";
}

.gallery-item {
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.gallery-item:hover {
  transform: scale(1.05);
}

.im1 {
  grid-area: im1;
}
.im2 {
  grid-area: im2;
}
.im3 {
  grid-area: im3;
}
.im4 {
  grid-area: im4;
}
.im5 {
  grid-area: im5;
}
.im6 {
  grid-area: im6;
}
.im7 {
  grid-area: im7;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-image {
  max-width: 90%;
  max-height: 90%;
  border-radius: 8px;
}
</style>
