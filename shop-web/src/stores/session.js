import { defineStore } from "pinia";

import { odooApi } from "../services/odooApi";

export const useSessionStore = defineStore("session", {
  state: () => ({
    loading: false,
    user: null,
    sessionInfo: null,
    authError: ""
  }),

  getters: {
    isLoggedIn(state) {
      return Boolean(state.user?.uid);
    },
    displayName(state) {
      if (!state.user) {
        return "Guest";
      }
      return state.user.name || state.user.login || "Account";
    }
  },

  actions: {
    async bootstrap() {
      this.loading = true;
      try {
        const info = await odooApi.getSessionInfo();
        this.sessionInfo = info;
        this.user = info && info.uid
          ? {
              uid: info.uid,
              name: info.name || info.username || "User",
              login: info.username || ""
            }
          : null;
      } finally {
        this.loading = false;
      }
    },

    async login({ login, password }) {
      this.loading = true;
      this.authError = "";
      try {
        const info = await odooApi.authenticate(login, password);
        this.sessionInfo = info;
        this.user = info && info.uid ? { uid: info.uid, name: info.name, login } : null;
        return this.user;
      } catch (error) {
        this.authError = error.message || "Login failed.";
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async logout() {
      this.loading = true;
      try {
        await odooApi.logout();
        this.user = null;
        this.sessionInfo = null;
      } finally {
        this.loading = false;
      }
    }
  }
});
