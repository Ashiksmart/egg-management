export type Role = "ADMIN" | "STAFF";

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: Role;
}

// Every backend response looks like this.
export interface ApiEnvelope<T> {
  data: T | null;
  meta: Record<string, unknown> | null;
  error: { code: string; message: string } | null;
}
