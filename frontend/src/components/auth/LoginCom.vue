<template>
  <div class="container-reg">
    <div class="container-left">
      <p>Ласкаво просимо на наш сайт новин!</p>
    </div>
    <div class="login-container">
      <div class="login-form">
        <h2>Вхід</h2>
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <input
              type="text"
              id="login-username"
              v-model="username"
              :class="{ 'input-field': true, error: !isValidUsername }"
              placeholder="Введіть логін"
            />
            <div class="error-message" v-if="showUsernameError">
              {{ usernameErrorMessage }}
            </div>
          </div>
          <div class="form-group">
            <input
              type="password"
              id="login-password"
              v-model="password"
              class="input-field"
              placeholder="Введіть пароль"
            />
            <div class="error-message" v-if="showPasswordError">
              {{ passwordErrorMessage }}
            </div>
          </div>
          <div class="form-actions gap-bot">
            <button type="submit" @click="login" class="login-button">
              Увійти
            </button>
          </div>
        </form>
        <div class="line"></div>
        <div class="have-account">
          Немає аккаунту? <a href="#/register">Реєстрація</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import axios from "axios";

export default {
  mounted() {
    if (localStorage.getItem("auth_token")) {
      localStorage.removeItem("auth_token");
      window.location.reload();
    }
  },
  data() {
    return {
      username: "",
      password: "",
      showUsernameError: false,
      showPasswordError: false,
      usernameErrorMessage: "Логін порожній",
      passwordErrorMessage: "Пароль порожній",
    };
  },
  computed: {
    isValidUsername() {
      return /^[a-zA-Z0-9_]+$/.test(this.username);
    },
  },
  methods: {
    parseData(data) {
      const parsedData = {};
      data[0].forEach((item) => {
        const [key, value] = item.split(":").map((str) => str.trim());
        parsedData[key] = value;
      });
      return parsedData;
    },
    login() {
      this.showUsernameError = false;
      this.showPasswordError = false;

      if (!this.username && !this.password) {
        this.showUsernameError = true;
        this.showPasswordError = true;
        return;
      } else if (!this.username) {
        this.showUsernameError = true;
        return;
      } else if (!this.password) {
        this.showPasswordError = true;
        return;
      }
    },
    async submitForm() {
      if (!this.isValidUsername) {
        Swal.fire({
          title: "Помилка",
          text: "Введіть правильний логін або пароль!",
          icon: "error",
        });
        return;
      }

      const formData = {
        username: this.username,
        password: this.password,
      };

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/users/authorization/token/login/",
          formData
        );

        if (response.status !== 200) {
          throw new Error("Invalid credentials");
        }

        const token = response.data.auth_token;
        axios.defaults.headers.common["Authorization"] = `Token ${token}`;

        const profileResponse = await axios.get(
          "http://127.0.0.1:8000/users/profile/",
          { headers: { Authorization: `Token ${token}` } }
        );

        const info = profileResponse.data.profile_information;

        if (!info || info.length === 0) {
          throw new Error("User profile not found");
        }

        const account_type = info[0].account_type;
        console.log(info);

        this.$store.commit("setToken", { token, account_type });

        Swal.fire({
          title: "Вітаю!",
          text: "Ви ввійшли в профіль!",
          icon: "success",
        }).then(() => {
          let route = "/profile";

          switch (account_type) {
            case "Читач":
              route = "/profile-reader/news";
              break;
            case "Журналіст":
              route = "/profile-journalist/my-news";
              break;
            case "Адміністратор":
              route = "/profile-admin/link";
              break;
          }

          this.$router.push(route).then(() => window.location.reload());
        });
      } catch (error) {
        console.error("Login failed:", error);

        let errorMessage = "Не вірний логін або пароль!";
        if (error.response?.status === 404) {
          errorMessage = "Не вдалося отримати інформацію про користувача!";
        } else if (error.response?.status === 401) {
          errorMessage = "Неправильний логін або пароль!";
        }

        Swal.fire({ icon: "error", text: errorMessage });
      }
    },
  },
};
</script>

<style>
.container-reg {
  max-width: 1100px;
  margin: 70px auto;
  display: flex;
  justify-content: space-between;
  gap: 50px;
  background-color: #e9effd;
  border-radius: 12px;
}
.container-left {
  background-image: url(../../assets/hero.png);
  width: 550px;
  height: 550px;
  border-radius: 12px 0 0 12px;
}
.container-left p {
  font-family: "Open Sans";
  font-style: normal;
  font-weight: 700;
  font-size: 16px;
  line-height: 30px;
  color: white;
  width: 250px;
  margin: 20px;
  background: rgba(0, 0, 0, 0.5);
  padding: 20px;
  border-radius: 8px;
}
.login-container {
  display: flex;
  align-items: center;
  width: 550px;
  height: 550px;
}
.login-form {
  width: 100%;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-form h2 {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
  font-family: "Roboto";
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

.input-field {
  width: 400px;
  padding: 12px;
  font-size: 16px;
  border: 2px solid #ccc;
  border-radius: 6px;
  transition: border-color 0.3s ease;
}

.input-field:focus {
  border-color: #4a90e2;
  outline: none;
}

.error-message {
  color: red;
  font-size: 14px;
  margin-top: 5px;
}

.login-button {
  width: 400px;
  padding: 12px;
  background-color: #4a90e2;
  color: white;
  font-size: 18px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #357abd;
}

.line {
  height: 1px;
  background-color: #ddd;
  margin: 20px 0;
}

.have-account {
  font-size: 14px;
}

.have-account a {
  color: #4a90e2;
  text-decoration: none;
  font-weight: bold;
}

.have-account a:hover {
  text-decoration: underline;
}
</style>
