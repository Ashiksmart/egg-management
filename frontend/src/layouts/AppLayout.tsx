import { useState } from "react";
import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

const NAV = [
  { to: "/", label: "Dashboard" },
  { to: "/purchases", label: "Purchases" },
  { to: "/inventory", label: "Inventory" },
  { to: "/sales", label: "Sales" },
  { to: "/customers", label: "Customers" },
  { to: "/suppliers", label: "Suppliers" },
  { to: "/transport", label: "Transport" },
  { to: "/wastage", label: "Wastage" },
  { to: "/payments", label: "Payments" },
  { to: "/expenses", label: "Expenses" },
  { to: "/reports", label: "Reports" },
  { to: "/settings", label: "Settings" },
];

// The 4 most-used screens sit in the phone's bottom bar; the rest are under "More".
const MOBILE_MAIN = ["/", "/sales", "/inventory", "/wastage"];

const linkClass = ({ isActive }: { isActive: boolean }) =>
  `block rounded-lg px-3 py-3 text-base font-medium ${
    isActive ? "bg-amber-100 text-amber-900" : "text-stone-700 hover:bg-stone-100"
  }`;

export default function AppLayout() {
  const { user, logout } = useAuth();
  const [moreOpen, setMoreOpen] = useState(false);

  return (
    <div className="min-h-screen md:flex">
      {/* Desktop sidebar */}
      <aside className="hidden w-60 shrink-0 flex-col border-r border-stone-200 bg-white p-4 md:flex">
        <h1 className="mb-4 text-lg font-bold text-amber-800">Egg Business</h1>
        <nav className="flex-1 space-y-1">
          {NAV.map((n) => (
            <NavLink key={n.to} to={n.to} end={n.to === "/"} className={linkClass}>
              {n.label}
            </NavLink>
          ))}
        </nav>
        <div className="border-t border-stone-200 pt-3 text-sm text-stone-600">
          <div className="truncate">{user?.email}</div>
          <button onClick={logout} className="mt-2 font-medium text-red-700">
            Log out
          </button>
        </div>
      </aside>

      <main className="flex-1 p-4 pb-24 md:p-8 md:pb-8">
        <Outlet />
      </main>

      {/* Phone bottom bar */}
      <nav className="fixed inset-x-0 bottom-0 z-20 grid grid-cols-5 border-t border-stone-200 bg-white md:hidden">
        {NAV.filter((n) => MOBILE_MAIN.includes(n.to)).map((n) => (
          <NavLink
            key={n.to}
            to={n.to}
            end={n.to === "/"}
            onClick={() => setMoreOpen(false)}
            className={({ isActive }) =>
              `py-4 text-center text-xs font-semibold ${isActive ? "text-amber-800" : "text-stone-600"}`
            }
          >
            {n.label}
          </NavLink>
        ))}
        <button
          onClick={() => setMoreOpen((o) => !o)}
          className="py-4 text-center text-xs font-semibold text-stone-600"
        >
          More
        </button>
      </nav>

      {moreOpen && (
        <div className="fixed inset-x-0 bottom-14 z-10 border-t border-stone-200 bg-white p-3 shadow-lg md:hidden">
          <div className="grid grid-cols-2 gap-2">
            {NAV.filter((n) => !MOBILE_MAIN.includes(n.to)).map((n) => (
              <NavLink key={n.to} to={n.to} className={linkClass} onClick={() => setMoreOpen(false)}>
                {n.label}
              </NavLink>
            ))}
          </div>
          <button onClick={logout} className="mt-3 w-full py-3 font-medium text-red-700">
            Log out ({user?.email})
          </button>
        </div>
      )}
    </div>
  );
}
