<template>
  <div class="contacts-container">
    <section class="section section-3">
      <div class="container-main flex-col">
        <h2>Про нас</h2>
        <p>
          Вітаємо на {{ websiteInfo.website_name }}! Ми завжди раді зв'язатися з
          вами.
        </p>
      </div>
    </section>

    <div class="contacts-grid" v-if="websiteInfo">
      <div class="contact-item">
        <i class="fas fa-phone contact-icon"></i>
        <h3>Телефон</h3>
        <p>{{ websiteInfo.phone_number }}</p>
      </div>
      <div class="contact-item">
        <i class="fas fa-envelope contact-icon"></i>
        <h3>Електронна пошта</h3>
        <p>{{ websiteInfo.email }}</p>
      </div>
      <div class="contact-item">
        <i class="fas fa-map-marker-alt contact-icon"></i>
        <h3>Адреса</h3>
        <p>{{ websiteInfo.address }}</p>
      </div>
    </div>

    <div class="social-links" v-if="websiteInfo">
      <h2>Соціальні мережі</h2>
      <a :href="websiteInfo.facebook" target="_blank"
        ><i class="fab fa-facebook"></i> Facebook</a
      >
      <a :href="websiteInfo.linkedin" target="_blank"
        ><i class="fab fa-linkedin"></i> LinkedIn</a
      >
      <a :href="websiteInfo.instagram" target="_blank"
        ><i class="fab fa-instagram"></i> Instagram</a
      >
      <a :href="websiteInfo.x" target="_blank"
        ><i class="fab fa-twitter"></i> X (Twitter)</a
      >
    </div>

    <div class="map-container" v-if="websiteInfo">
      <iframe
        :src="websiteInfo.google_map"
        width="100%"
        height="400"
        style="border: 0"
        allowfullscreen=""
        loading="lazy"
      ></iframe>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "WebsiteInfoPage",
  data() {
    return {
      websiteInfo: [],
    };
  },
  mounted() {
    this.fetchWebsiteInfo();
  },
  methods: {
    async fetchWebsiteInfo() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/website_info/website_information/"
        );

        if (
          response.status === 200 &&
          response.data.website_information?.length > 0
        ) {
          this.websiteInfo = response.data.website_information[0];
        } else {
          console.warn("No website information available.");
        }
      } catch (error) {
        if (error.response?.status === 404) {
          console.warn("Website information not found.");
        } else {
          console.error("Error fetching website information:", error);
        }
      }
    },
  },
};
</script>

<style scoped>
.contacts-container {
  font-family: Arial, sans-serif;
  color: #fff;
  background-color: #00274d;
  padding: 40px 0;
  text-align: center;
}

.section-3 {
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 10px;
  margin: 20px auto;
  max-width: 650px;
}

.contacts-grid {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.contact-item {
  background: white;
  color: black;
  border-radius: 10px;
  padding: 15px;
  text-align: center;
  width: 350px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.contact-icon {
  font-size: 24px;
  margin-bottom: 10px;
  color: #00274d;
}

.social-links {
  margin-top: 60px;
}

.social-links a {
  display: inline-block;
  margin: 5px;
  color: #ffcc00;
  text-decoration: none;
  font-weight: bold;
}

.social-links a i {
  margin-right: 8px;
}

.social-links a:hover {
  color: #e6b800;
}

.map-container {
  margin-top: 20px;
}
</style>
