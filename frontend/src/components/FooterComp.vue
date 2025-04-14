<template>
  <footer class="footer">
    <div class="container-foot">
      <div class="footer-content">
        <div class="footer-column">
          <p class="slogan">Останні новини Стрия - будь у курсі подій!</p>
          <div class="social-links">
            <a :href="websiteInfo.facebook" target="_blank"
              ><i class="fab fa-facebook"></i
            ></a>
            <a :href="websiteInfo.linkedin" target="_blank"
              ><i class="fab fa-linkedin"></i
            ></a>
            <a :href="websiteInfo.instagram" target="_blank"
              ><i class="fab fa-instagram"></i
            ></a>
            <a :href="websiteInfo.x" target="_blank"
              ><i class="fab fa-twitter"></i
            ></a>
          </div>
        </div>

        <div class="footer-column">
          <h3>Останні новини</h3>
          <ul>
            <li v-if="loading">Завантаження новин...</li>
            <li v-else-if="news.length === 0">Новини відсутні.</li>
            <li v-for="item in news.slice(0, 3)" :key="item.id">
              <router-link :to="`/news/${item.id}`">{{
                item.title
              }}</router-link>
            </li>
          </ul>
        </div>

        <div class="footer-column">
          <h3>Корисні посилання</h3>
          <ul>
            <li><router-link to="/">Головна</router-link></li>
            <li><router-link to="/categories">Категорії</router-link></li>
            <li><router-link to="/contacts">Контакти</router-link></li>
          </ul>
        </div>
      </div>

      <div class="footer-line"></div>

      <div class="footer-bottom">
        <p>© 2025 Новини Стрия. Усі права захищені.</p>
      </div>
    </div>
  </footer>
</template>

<script>
import axios from "axios";

export default {
  name: "FooterComp",
  data() {
    return {
      news: [],
      loading: true,
      websiteInfo: {},
    };
  },
  async created() {
    await this.fetchWebsiteInfo();
    await this.fetchLatestNews();
  },
  watch: {
    "$route.params.id": {
      handler() {
        this.fetchLatestNews();
      },
      immediate: true,
    },
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
        console.error("Error fetching website information:", error);
      }
    },
    async fetchLatestNews() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/news/last_six_news_info/"
        );
        console.log("Новини:", response.data);
        if (
          response.status === 200 &&
          Array.isArray(response.data.last_six_news_info)
        ) {
          this.news = response.data.last_six_news_info.sort(
            (a, b) =>
              new Date(b.date_of_last_update) - new Date(a.date_of_last_update)
          );
          console.log(this.news);
        } else {
          console.warn("Новини не знайдено.");
          this.news = [];
        }
      } catch (error) {
        console.error("Помилка завантаження новин:", error);
        this.news = [];
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.footer {
  background: linear-gradient(to top, #0d1b2a, #00274d);
  padding: 30px 20px;
  text-align: center;
  color: white;
}

.container-foot {
  max-width: 1100px;
  margin: 0 auto;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  gap: 30px;
  flex-wrap: wrap;
}

.footer-column {
  flex: 1;
  min-width: 250px;
}

.footer-column h3 {
  font-size: 18px;
  margin-bottom: 10px;
}

.footer-column ul {
  list-style: none;
  padding: 0;
}

.footer-column ul li {
  margin-bottom: 8px;
}

.footer-column ul li a {
  text-decoration: none;
  color: #ffffff;
  font-size: 16px;
  transition: color 0.3s;
}

.footer-column ul li a:hover {
  color: #f8b400;
}

.slogan {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 15px;
}

.social-links a {
  margin: 0 10px;
  font-size: 1.5rem;
  color: white;
  transition: color 0.3s;
}

.social-links a:hover {
  color: #f8b400;
}

.footer-line {
  width: 100%;
  height: 1px;
  background-color: #ffffff;
  margin: 20px 0;
}

.footer-bottom {
  font-size: 14px;
}
</style>
