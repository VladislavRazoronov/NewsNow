<template>
  <div v-if="isAuthenticated" class="profile-container back-wh relat-stud">
    <div class="profile-info-section">
      <div class="profile-info-row">
        <label for="user-username">Логін</label>
        <div class="cols-rev">
          <input
            id="user-username"
            type="text"
            v-model="user.username"
            @input="usernameInput"
            required
          />
          <div
            v-if="!isValidUsername() && usernameTouched"
            class="error-message"
          >
            Логін не підходить
          </div>
        </div>
      </div>
      <div class="profile-info-row">
        <label for="user-email">Електронна пошта</label>
        <div class="cols-rev">
          <input
            id="user-email"
            type="email"
            v-model="user.email"
            @input="emailInput"
            required
          />
          <span v-if="!isValidEmail() && emailTouched" class="error-message"
            >Введіть справжній email</span
          >
        </div>
      </div>
      <div class="profile-info-row">
        <label for="user-phone">Номер телефону</label>
        <div class="cols-rev">
          <input
            id="user-phone"
            type="text"
            v-model="user.phoneNumber"
            required
          />
          <span v-if="!isValidPhoneNumber()" class="error-message"
            >Введіть справжній номер телефону</span
          >
        </div>
      </div>
      <div class="profile-info-row">
        <label for="user-firstname">Ім'я</label>
        <div class="cols-rev">
          <input
            id="user-firstname"
            type="text"
            v-model="user.firstName"
            required
          />
          <span v-if="!isValidFirstName()" class="error-message"
            >Введіть справжнє ім'я</span
          >
        </div>
      </div>
      <div class="profile-info-row">
        <label for="user-patronymic">По-батькові</label>
        <div class="cols-rev">
          <input
            id="user-patronymic"
            type="text"
            v-model="user.patronymic"
            required
          />
          <span v-if="!isValidPatronymic()" class="error-message">
            Введіть справжнє по-батькові
          </span>
        </div>
      </div>

      <div class="profile-info-row">
        <label for="user-lastname">Прізвище</label>
        <div class="cols-rev">
          <input
            id="user-lastname"
            type="text"
            v-model="user.lastName"
            required
          />
          <span v-if="!isValidLastName()" class="error-message"
            >Введіть справжнє прізвище</span
          >
        </div>
      </div>
      <div class="profile-info-row">
        <label for="user-dob">Дата народження</label>
        <div class="cols-rev">
          <input
            id="user-dob"
            type="date"
            v-model="user.birthday"
            required
            :class="{ invalid: !isValidBirthdate }"
          />
        </div>
        <p v-if="!isValidBirthdate" class="error-message">
          Невірна дата народження
        </p>
      </div>

      <button class="update-profile-user gap-bottom" @click="updateProfile">
        Оновити профіль
      </button>
    </div>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import axios from "axios";
import { mapGetters } from "vuex";

export default {
  computed: {
    ...mapGetters(["isAuthenticated"]),
  },
  data() {
    return {
      selectedFile: null,
      initialUsername: "",
      initialEmail: "",
      initialfirstName: "",
      initiallastName: "",
      initialPatronymic: "",
      initialPhoneNumber: "",
      targetImagePath: "@/../../backend/user_images/",
      user: {
        username: "",
        email: "",
        phoneNumber: "",
        photo: "",
        image: "",
        firstName: "",
        lastName: "",
        patronymic: "",
      },
      usernameTouched: false,
      emailTouched: false,
    };
  },

  mounted() {
    const token = this.$store.state.token;

    if (!token) {
      console.error("Token is missing! Redirecting to login.");
      this.$router.push("/login");
      return;
    }

    axios
      .get("http://127.0.0.1:8000/users/profile/", {
        headers: {
          Authorization: `Token ${token}`,
        },
      })
      .then((response) => {
        if (response.status !== 200) {
          throw new Error(`Unexpected response status: ${response.status}`);
        }

        if (!response.data || !response.data.profile_information) {
          throw new Error("Invalid profile data received.");
        }

        const info = response.data.profile_information[0];

        this.user.username = info.username || "";
        this.user.email = info.email || "";
        this.user.photo = info.image || "";
        this.user.phoneNumber = info.phone_number || "";
        this.user.firstName = info.first_name || "";
        this.user.lastName = info.last_name || "";
        this.user.patronymic = info.patronymic || "";

        this.initialUsername = this.user.username;
        this.initialEmail = this.user.email;
        this.initialfirstName = this.user.firstName;
        this.initiallastName = this.user.lastName;
        this.initialPatronymic = this.user.patronymic;
        this.initialPhoneNumber = this.user.phoneNumber;
      })
      .catch((error) => {
        console.error("Error fetching profile:", error);

        if (error.response) {
          if (error.response.status === 404) {
            Swal.fire({
              icon: "error",
              title: "Помилка!",
              text: "Профіль не знайдено!",
            }).then(() => {
              this.$router.push("/login");
            });
          } else if (error.response.status === 401) {
            Swal.fire({
              icon: "error",
              title: "Сесія закінчилася!",
              text: "Будь ласка, увійдіть знову.",
            }).then(() => {
              this.$store.commit("logout");
              this.$router.push("/login");
            });
          } else {
            Swal.fire({
              icon: "error",
              title: "Помилка!",
              text: `Сталася помилка: ${error.response.statusText} (${error.response.status})`,
            });
          }
        } else {
          Swal.fire({
            icon: "error",
            title: "Помилка!",
            text: "Не вдалося завантажити профіль. Спробуйте пізніше.",
          });
        }
      });
  },

  methods: {
    isValidUsername() {
      return /^[a-zA-Z0-9_]+$/.test(this.user.username);
    },
    isValidEmail() {
      if (this.user.email === "") {
        return false;
      }
      return /^([a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,}))?$/.test(
        this.user.email
      );
    },
    isValidPhoneNumber() {
      if (this.user.phoneNumber === "") {
        return false;
      }
      return /^(\+(?:[0-9] ?){12,12}[0-9]*)?$/.test(this.user.phoneNumber);
    },
    isValidFirstName() {
      return /^([А-ЩЬЮЯҐЄІЇ][а-щьюяґєії']{1,20})([-][А-ЩЬЮЯҐЄІЇ][а-щьюяґєії']{1,20}){0,2}$/.test(
        this.user.firstName
      );
    },
    isValidLastName() {
      return /^([А-ЩЬЮЯҐЄІЇ][а-щьюяґєії']{1,20})([-][А-ЩЬЮЯҐЄІЇ][а-щьюяґєії']{1,20}){0,2}$/.test(
        this.user.lastName
      );
    },
    isValidPatronymic() {
      return /^([А-ЩЬЮЯҐЄІЇ][а-щьюяґєії']{1,20})$/.test(this.user.patronymic);
    },

    isFormValid() {
      return this.isValidUsername() && this.isValidEmail();
    },
    updateProfile() {
      if (this.isFormValid()) {
        Swal.fire({
          icon: "question",
          title: "Ви впевнені, що хочете оновити профіль?",
          showCancelButton: true,
          confirmButtonText: "Так",
          cancelButtonText: "Ні",
        }).then((result) => {
          if (result.isConfirmed) {
            const isLoginChanged = this.user.username == this.initialUsername;
            const isEmailChanged = this.user.email == this.initialEmail;
            const isPhoneNumberChanged =
              this.user.phoneNumber == this.initialPhoneNumber;
            const isFNChanged = this.user.firstName == this.initialfirstName;
            const isLNChanged = this.user.lastName == this.initiallastName;
            const isPChanged = this.user.patronymic == this.initialPatronymic;

            if (
              !isLoginChanged &&
              !isEmailChanged &&
              !isPhoneNumberChanged &&
              !isFNChanged &&
              !isLNChanged &&
              !isPChanged
            ) {
              Swal.fire({
                icon: "error",
                title: "Помилка!",
                text: "Ви не внесли жодних змін!",
              });
              return;
            }

            const requestData = {
              new_username: this.user.username,
              new_email: this.user.email,
              new_phone_number: this.user.phoneNumber,
              new_first_name: this.user.firstName,
              new_last_name: this.user.lastName,
              new_patronymic: this.user.patronymic,
              current_username: isLoginChanged,
              current_email: isEmailChanged,
              current_phone_number: isPhoneNumberChanged,
            };

            console.log(requestData);
            const token = this.$store.state.token;
            axios
              .post(
                "http://127.0.0.1:8000/users/update_profile/",
                requestData,
                {
                  headers: {
                    Authorization: `Token ${token}`,
                  },
                }
              )
              .then((response) => {
                console.log(response);
                if (response.status === 200) {
                  Swal.fire({
                    icon: "success",
                    title: "Профіль оновлено!",
                  }).then(() => {
                    window.location.reload();
                  });
                } else if (
                  response.data.Message === "username is already taken!"
                ) {
                  Swal.fire({
                    icon: "error",
                    title: "Помилка!",
                    text: "Логін вже зайнятий!",
                  });
                } else if (
                  response.data.Message === "email is already taken!"
                ) {
                  Swal.fire({
                    icon: "error",
                    title: "Помилка!",
                    text: "Електронна пошта вже зайнята!",
                  });
                } else if (
                  response.data.Message === "phone number is already taken!"
                ) {
                  Swal.fire({
                    icon: "error",
                    title: "Помилка!",
                    text: "Номер телефону вже зайнятий!",
                  });
                } else {
                  Swal.fire({
                    icon: "error",
                    title: "Помилка!",
                    text: "Не вдалося оновити профіль. Спробуйте пізніше!",
                  });
                }
              })
              .catch((error) => {
                console.error("Error updating profile:", error);
                Swal.fire({
                  icon: "error",
                  title: "Помилка!",
                  text: "Не вдалося оновити профіль. Спробуйте пізніше!",
                });
              });
          }
        });
      } else {
        Swal.fire({
          icon: "error",
          title: "Помилка!",
          text: "Заповніть всі поля правильно!",
        });
      }
    },
    usernameInput() {
      this.usernameTouched = true;
    },
    emailInput() {
      this.emailTouched = true;
    },
  },
};
</script>

<style scoped>
.profile-container {
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
}
.profile-picture-preview {
  border-radius: 50%;
  margin: 0 auto;
  object-fit: cover;
  display: flex;
  width: 200px;
  height: 200px;
  border: 2px solid black;
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1);
}
.profile-info-section {
  flex: 1;
  margin: 0 auto;
}
.profile-info-row {
  margin-bottom: 20px;
}
.profile-info-row label {
  display: block;
  font-weight: bold;
  margin-bottom: 7px;
}

.profile-info-row input {
  width: calc(100% - 40px);
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.error-message {
  color: #e74c3c;
  font-size: 14px;
  margin-top: 5px;
}
.update-profile-user {
  background-color: #007bff;
  color: #fff;
  margin: 0 auto;
  display: flex;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  cursor: pointer;
}
.update-profile-user:hover {
  background-color: #0056b3;
}
</style>
