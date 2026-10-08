import { useEffect, useState } from "react";
import { api } from "../services/api";

export default function Dashboard() {
  const [status, setStatus] = useState("checking...");

  // Phase 1 only proves the phone/browser can talk to the backend.
  useEffect(() => {
    api<{ status: string }>("/health")
      .then((d) => setStatus(d.status))
      .catch((e: Error) => setStatus(`error: ${e.message}`));
  }, []);

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">Dashboard</h2>
      <div className="rounded-2xl bg-white p-5 shadow-sm">
        <p className="text-sm text-stone-600">Server status</p>
        <p className="text-xl font-semibold">{status}</p>
      </div>
      <p className="text-sm text-stone-600">
        KPI cards and charts arrive in later phases, once purchases and sales exist.
      </p>
    </div>
  );
}
