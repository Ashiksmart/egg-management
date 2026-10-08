import { Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "./hooks/useAuth";
import AppLayout from "./layouts/AppLayout";
import ComingSoon from "./pages/ComingSoon";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";

// [path, title, phase it will be built in]
const PLACEHOLDERS: [string, string, number][] = [
  ["purchases", "Purchases", 3],
  ["inventory", "Inventory", 3],
  ["sales", "Sales", 4],
  ["customers", "Customers", 2],
  ["suppliers", "Suppliers", 2],
  ["transport", "Transport", 7],
  ["wastage", "Wastage", 5],
  ["payments", "Payments", 6],
  ["expenses", "Expenses", 8],
  ["reports", "Reports", 9],
  ["settings", "Settings", 2],
];

function RequireAuth({ children }: { children: JSX.Element }) {
  const { user, loading } = useAuth();
  if (loading) return <p className="p-6 text-stone-600">Loading...</p>;
  if (!user) return <Navigate to="/login" replace />;
  return children;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        element={
          <RequireAuth>
            <AppLayout />
          </RequireAuth>
        }
      >
        <Route index element={<Dashboard />} />
        {PLACEHOLDERS.map(([path, title, phase]) => (
          <Route key={path} path={path} element={<ComingSoon title={title} phase={phase} />} />
        ))}
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
