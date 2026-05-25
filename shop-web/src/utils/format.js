import { currentLocale, SUPPORTED_LOCALES } from "../i18n";

const DEFAULT_CURRENCY = "USD";

function currencyForLocale() {
  const code = currentLocale();
  const entry = SUPPORTED_LOCALES.find((l) => l.code === code);
  return entry?.currency || DEFAULT_CURRENCY;
}

export function formatMoney(value, currency) {
  const cur = currency || currencyForLocale();
  const code = currentLocale();
  const intl = code === "zh" ? "zh-CN" : "en-US";
  return new Intl.NumberFormat(intl, {
    style: "currency",
    currency: cur
  }).format(Number(value || 0));
}

export function formatDate(value) {
  if (!value) return "";
  const code = currentLocale();
  const intl = code === "zh" ? "zh-CN" : "en-US";
  const d = typeof value === "string" ? new Date(value) : value;
  if (Number.isNaN(d.getTime())) return String(value);
  return new Intl.DateTimeFormat(intl, {
    dateStyle: "medium",
    timeStyle: "short"
  }).format(d);
}
