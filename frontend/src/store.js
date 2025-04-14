import { createStore } from "vuex";

export default createStore({
  state: {
    token: "",
    account_type: "",
  },
  mutations: {
    setToken(state, { token, account_type }) {
      state.token = token;
      state.account_type = account_type;
      localStorage.setItem("auth_token", token);
      localStorage.setItem("account_type", account_type);
    },

    removeToken(state) {
      state.token = "";
      state.account_type = "";
      localStorage.removeItem("auth_token");
      localStorage.removeItem("account_type");
    },

    initializeStore(state) {
      const token = localStorage.getItem("auth_token");
      const account_type = localStorage.getItem("account_type");
      if (token) {
        state.token = token;
        state.account_type = account_type;
      }
    },
  },
  getters: {
    isAuthenticated: (state) => {
      return state.token !== "";
    },
    account_type: (state) => state.account_type,
  },
  actions: {},
  modules: {},
});
