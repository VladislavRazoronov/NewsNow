import { createRouter, createWebHashHistory } from "vue-router";
import store from "../store";

// usual
import Home from "../components/HomePage.vue";
import Contacts from "../components/ContactsPage.vue";
import NotFound from "../components/NotFound.vue";

import CategoriesComp from "@/components/categories/CategoriesComp.vue";
import NewsCategories from "@/components/categories/NewsCategories.vue";
import NewsComp from "@/components/categories/NewsComp.vue";

// auth
import Login from "../components/auth/LoginCom.vue";
import Register from "../components/auth/RegisterCom.vue";

import userReader from "../components/userReader/ProfileCom.vue";
import ProfileSettingsReader from "../components/userReader/profile/ProfileDetails.vue";
import ReaderNews from "../components/userReader/profile/ReaderNews.vue";

import userJournalist from "../components/userJournalist/ProfileCom.vue";
import ProfileSettingsJournalist from "../components/userJournalist/profile/ProfileDetails.vue";
import CreatedNews from "../components/userJournalist/profile/CreatedNews.vue";
import AddNews from "../components/userJournalist/profile/AddNews.vue";
import EditNews from "../components/userJournalist/profile/EditNews.vue";

import userAdmin from "../components/userAdmin/ProfileCom.vue";
import ProfileSettingsAdmin from "../components/userAdmin/profile/ProfileDetails.vue";
import ProfileLink from "../components/userAdmin/profile/ProfileLink.vue";

const routes = [
  { path: "/", component: Home, meta: { title: "Головна - NewsNow" } },
  {
    path: "/contacts",
    component: Contacts,
    meta: { title: "Контакти | NewsNow" },
  },
  {
    path: "/categories",
    component: CategoriesComp,
    meta: { title: "Категорії новин - NewsNow" },
  },
  {
    path: "/categories_news/:id?",
    component: NewsCategories,
    meta: { title: "Новини категорії - NewsNow" },
  },
  {
    path: "/news/:id?",
    component: NewsComp,
    meta: { title: "Новина - NewsNow" },
  },
  { path: "/login", component: Login, meta: { title: "Логін | NewsNow" } },
  {
    path: "/register",
    component: Register,
    meta: { title: "Реєстрація | NewsNow" },
  },
  {
    path: "/profile-reader",
    component: userReader,
    meta: {
      title: "Профіль | NewsNow",
      requiresAuth: true,
      roles: ["Читач"],
    },
    children: [
      { path: "settings", component: ProfileSettingsReader },
      { path: "news", component: ReaderNews },
    ],
  },
  {
    path: "/profile-journalist",
    component: userJournalist,
    meta: {
      title: "Профіль | NewsNow",
      requiresAuth: true,
      roles: ["Журналіст"],
    },
    children: [
      { path: "settings", component: ProfileSettingsJournalist },
      { path: "my-news", component: CreatedNews },
      { path: "add-news", component: AddNews },
      { path: "edit-news/:id?", component: EditNews },
    ],
  },
  {
    path: "/profile-admin",
    component: userAdmin,
    meta: {
      title: "Профіль | NewsNow",
      requiresAuth: true,
      roles: ["Адміністратор"],
    },
    children: [
      { path: "settings", component: ProfileSettingsAdmin },
      { path: "link", component: ProfileLink },
    ],
  },
  {
    path: "/:pathMatch(.*)*",
    component: NotFound,
    meta: { title: "Сторінки не знайдено | NewsNow" },
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior() {
    return { top: 0, behavior: "smooth" };
  },
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated;
  const account_type = store.getters.account_type;

  if ((to.path === "/login" || to.path === "/register") && isAuthenticated) {
    next("/");
    return;
  }

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next("/login");
    } else if (
      to.matched.some(
        (record) =>
          record.meta.roles && !record.meta.roles.includes(account_type)
      )
    ) {
      next("/");
    } else {
      next();
    }
  } else {
    next();
  }
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || "Стрий";
  next();
});

export default router;
