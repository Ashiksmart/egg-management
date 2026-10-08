import { useState, type FormEvent } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function Login() {
  const { user, login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  if (user) return <Navigate to="/" replace />;

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await login(email.trim(), password);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed.");
    } finally {
      setBusy(false);
    }
  }

  const input =
    "w-full rounded-lg border border-stone-300 bg-white px-4 py-3 text-base focus:border-amber-600 focus:outline-none";

  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <form onSubmit={onSubmit} className="w-full max-w-sm space-y-4 rounded-2xl bg-white p-6 shadow">
        <h1 className="text-2xl font-bold text-amber-800">Egg Business</h1>
        <p className="text-sm text-stone-600">Log in to continue.</p>
        <input
          className={input}
          type="email"
          inputMode="email"
          autoComplete="username"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          className={input}
          type="password"
          autoComplete="current-password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {error && <p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
        <button
          disabled={busy}
          className="w-full rounded-lg bg-amber-700 py-3 text-base font-semibold text-white disabled:opacity-60"
        >
          {busy ? "Logging in..." : "Log in"}
        </button>
      </form>
    </div>
  );
}
