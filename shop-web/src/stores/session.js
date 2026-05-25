import { defineStore } from "pinia";

import { odooApi } from "../services/odooApi";

export const useSessionStore = defineStore("session", {
  state: () => ({
    loading: false,
    user: null,
    sessionInfo: null,
    profile: null,
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

    async register({ name, login, password, phone }) {
      this.loading = true;
      this.authError = "";
      try {
        const info = await odooApi.register({ name, login, password, phone });
        this.user = info && info.uid ? { uid: info.uid, name: info.name, login } : null;
        this.sessionInfo = info;
        return this.user;
      } catch (error) {
        this.authError = error.message || "Registration failed.";
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async forgotPassword(login) {
      this.authError = "";
      try {
        return await odooApi.passwordForgot(login);
      } catch (error) {
        this.authError = error.message || "Password reset request failed.";
        throw error;
      }
    },

    async resetPassword({ token, login, newPassword }) {
      this.loading = true;
      this.authError = "";
      try {
        const result = await odooApi.passwordReset({ token, login, newPassword });
        await this.bootstrap();
        return result;
      } catch (error) {
        this.authError = error.message || "Password reset failed.";
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async changePassword({ currentPassword, newPassword }) {
      this.loading = true;
      this.authError = "";
      try {
        return await odooApi.changePassword({ currentPassword, newPassword });
      } catch (error) {
        this.authError = error.message || "Change password failed.";
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async loadProfile() {
      if (!this.isLoggedIn) {
        return null;
      }
      try {
        this.profile = await odooApi.getProfile();
        return this.profile;
      } catch (error) {
        return null;
      }
    },

    async updateProfile(payload) {
      this.loading = true;
      try {
        const result = await odooApi.updateProfile(payload);
        if (this.profile) {
          this.profile = { ...this.profile, ...result };
        }
        if (this.user && result.name) {
          this.user = { ...this.user, name: result.name };
        }
        return result;
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
        this.profile = null;
      } finally {
        this.loading = false;
      }
    }
  }
});
