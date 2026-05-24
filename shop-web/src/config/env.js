const rawBaseUrl = import.meta.env.VITE_ODOO_BASE_URL || "http://127.0.0.1:8069";
const useProxy = String(import.meta.env.VITE_ODOO_USE_PROXY || "false") === "true";

export const odooEnv = {
  baseUrl: rawBaseUrl.replace(/\/$/, ""),
  db: import.meta.env.VITE_ODOO_DB || "",
  useProxy
};

export function resolveOdooUrl(path) {
  if (odooEnv.useProxy) {
    return path;
  }
  if (!path.startsWith("/")) {
    return `${odooEnv.baseUrl}/${path}`;
  }
  return `${odooEnv.baseUrl}${path}`;
}
