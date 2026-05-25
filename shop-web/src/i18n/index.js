import { createI18n } from "vue-i18n";

import en from "../locales/en.json";
import zh from "../locales/zh.json";

const STORAGE_KEY = "odoo_shop_locale";

function detect() {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored) return stored;
  const browser = (navigator.language || "en").toLowerCase();
  if (browser.startsWith("zh")) return "zh";
  return "en";
}

export const SUPPORTED_LOCALES = [
  { code: "en", label: "English", currency: "USD" },
  { code: "zh", label: "中文", currency: "CNY" }
];

export const i18n = createI18n({
  legacy: false,
  globalInjection: true,
  locale: detect(),
  fallbackLocale: "en",
  messages: { en, zh }
});

export function setLocale(code) {
  if (!code) return;
  i18n.global.locale.value = code;
  localStorage.setItem(STORAGE_KEY, code);
  document.documentElement.lang = code;
}

export function currentLocale() {
  return i18n.global.locale.value;
}
