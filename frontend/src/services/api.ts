import type { ApiEnvelope } from "../types";

const TOKEN_KEY = "egg_token";

export const tokenStore = {
  get: () => localStorage.getItem(TOKEN_KEY),
  set: (t: string) => localStorage.setItem(TOKEN_KEY, t),
  clear: () => localStorage.removeItem(TOKEN_KEY),
};

export class ApiError extends Error {
  code: string;
  status: number;
  constructor(code: string, message: string, status: number) {
    super(message);
    this.code = code;
    this.status = status;
  }
}

export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");
  const token = tokenStore.get();
  if (token) headers.set("Authorization", `Bearer ${token}`);

  let res: Response;
  try {
    res = await fetch(`/api/v1${path}`, { ...options, headers });
  } catch {
    throw new ApiError("NETWORK", "Cannot reach the server. Check your connection.", 0);
  }

  const body = (await res.json().catch(() => null)) as ApiEnvelope<T> | null;
  if (!res.ok || !body || body.error) {
    throw new ApiError(
      body?.error?.code ?? "UNKNOWN",
      body?.error?.message ?? "Something went wrong.",
      res.status,
    );
  }
  return body.data as T;
}
