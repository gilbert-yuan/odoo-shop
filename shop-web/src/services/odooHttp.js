import { resolveOdooUrl } from "../config/env";

let rpcId = 1;

async function requestJson(urlPath, payload, { withCredentials = true } = {}) {
  const response = await fetch(resolveOdooUrl(urlPath), {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: withCredentials ? "include" : "same-origin",
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`HTTP ${response.status}: ${text.slice(0, 300)}`);
  }

  const data = await response.json();
  if (data?.error) {
    const msg =
      data.error?.data?.message || data.error?.message || "Odoo RPC request failed.";
    throw new Error(msg);
  }
  return data.result;
}

export async function rpc(route, params = {}, options = {}) {
  return requestJson(
    route,
    {
      jsonrpc: "2.0",
      method: "call",
      params,
      id: rpcId++
    },
    options
  );
}

export async function callKw(model, method, args = [], kwargs = {}) {
  return rpc("/web/dataset/call_kw", {
    model,
    method,
    args,
    kwargs
  });
}

export async function callKwPath(model, method, args = [], kwargs = {}) {
  return rpc(`/web/dataset/call_kw/${model}/${method}`, {
    model,
    method,
    args,
    kwargs
  });
}
