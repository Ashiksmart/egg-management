# Egg Distribution Management System: Architecture Plan (Step 0)

Nothing is built yet. This is the plan for your approval. Language is kept simple on purpose.

---

## 1. System Architecture

```
Android phone / Desktop browser
        |  (HTTPS)
React + TypeScript (Vite, Tailwind, shadcn/ui, Recharts)
        |  REST + JSON, JWT token
FastAPI (Python)
  api/        -> routes only (thin)
  schemas/    -> Pydantic validation
  services/   -> business rules (landed cost, FEFO, closing)
  repositories/ -> database queries
  models/     -> SQLAlchemy tables
        |
PostgreSQL (NUMERIC for money, Alembic migrations)
```

Key design decisions:
- **Business rules live only in `services/`**, never in the UI. Tests target this layer.
- **Inventory is a ledger.** Stock is never "edited"; every change is a row in `inventory_transactions`. Current stock = sum of rows.
- **Money = Decimal / NUMERIC(14,2)**, rates = NUMERIC(10,4). Never float.
- **Soft delete** (`deleted_at`) on all financial tables. Nothing is physically removed.
- **Audit log** written by the service layer on every create/edit/delete.
- **Extensible hooks**: `warehouse_id` and `business_id` columns are NOT added now, but all code goes through repositories, so adding them later is a contained change.

## 2. ER Diagram

```mermaid
erDiagram
  USER ||--o{ AUDIT_LOG : writes
  SUPPLIER ||--o{ PURCHASE : supplies
  PURCHASE ||--|{ PURCHASE_ITEM : has
  PURCHASE_ITEM ||--|| BATCH : creates
  TRANSPORT ||--o{ TRANSPORT_ALLOCATION : splits_into
  BATCH ||--o{ TRANSPORT_ALLOCATION : receives
  BATCH ||--o{ INVENTORY_TXN : moves
  CUSTOMER ||--o{ SALE : buys
  SALE ||--|{ SALE_ITEM : has
  SALE_ITEM }o--|| BATCH : drawn_from
  SALE ||--o| DELIVERY : delivered_by
  DELIVERY }o--|| ROUTE : on
  CUSTOMER ||--o{ LEDGER_ENTRY : has
  SALE ||--o{ PAYMENT_ALLOCATION : paid_by
  PAYMENT ||--o{ PAYMENT_ALLOCATION : applied_to
  PAYMENT }o--o| CUSTOMER : from
  PAYMENT }o--o| SUPPLIER : to
  BATCH ||--o{ WASTAGE : loses
  WASTAGE }o--|| WASTAGE_CATEGORY : reason
  EXPENSE }o--|| EXPENSE_CATEGORY : type
  DAILY_CLOSING ||--o{ DAILY_CLOSING_LINE : per_batch
```

## 3. Database Schema Proposal

Common columns on every table: `id` (PK), `created_at`, `updated_at`, `created_by`. Financial tables also `deleted_at`, `deleted_by`.

| Table | Important columns | Constraints / indexes |
|---|---|---|
| users | email, password_hash, role (ADMIN/STAFF), is_active | unique(email) |
| settings | key, value (JSON) | unique(key). Eggs/petti, eggs/tray, wastage target, invoice prefix, etc. |
| suppliers | name, contact, phone, whatsapp, location, egg_type, egg_size, current_rate, payment_terms, upi, is_active | index(name) |
| customers | name, type (WHOLESALE/B2B/RETAIL), phone, credit_days, daily_requirement, delivery_time, route_id, opening_balance | index(name, type) |
| purchases | purchase_no, supplier_id, date, loading, packing, local_transport, other_cost, total_cost, payment_status | unique(purchase_no), index(date) |
| purchase_items | purchase_id, egg_size, qty_eggs, qty_petti, qty_trays, loose, rate_per_egg | qty_eggs = computed and stored |
| batches | batch_code, purchase_item_id, supplier_id, received_qty, damaged_on_arrival, sellable_qty, purchase_rate, landed_cost_total, landed_cost_per_egg, arrival_at, status | unique(batch_code), index(status, arrival_at) |
| transports | transport_no, date, vehicle, driver, provider, freight, loading, unloading, other, total, payment_status | |
| transport_allocations | transport_id, batch_id, eggs, allocated_cost | one shipment can feed many batches |
| inventory_txns | batch_id, type (PURCHASE/SALE/WASTAGE/RETURN/ADJUSTMENT), qty (+/-), ref_type, ref_id, reason, txn_at | index(batch_id, txn_at). Append-only |
| sales | invoice_no, customer_id, sale_type, date, gross, discount, delivery_charge, net_total, paid, balance, due_date | unique(invoice_no), index(date, customer_id) |
| sale_items | sale_id, batch_id, qty, rate, cost_per_egg_snapshot | snapshot gives exact COGS |
| payments | direction (IN/OUT), party_type, customer_id/supplier_id, amount, method, reference, date | index(date) |
| payment_allocations | payment_id, sale_id/purchase_id/transport_id, amount | lets one payment settle many invoices |
| ledger_entries | customer_id, date, ref, debit, credit, running_balance | index(customer_id, date) |
| wastage_categories | code (W1..W8), name | seeded |
| wastage | batch_id, category_id, qty, location, cost_per_egg, total_loss, notes, photo_url | check(qty > 0) |
| expense_categories / expenses | date, category_id, amount, method, description, receipt_url | |
| routes / deliveries / delivery_items | route stops, driver, status, delivered_at | |
| daily_closings | date, status (OPEN/CLOSED), opening, purchases, sales, wastage, expected, physical, variance, reason | unique(date) |
| audit_logs | user_id, action, entity, entity_id, old_value (JSON), new_value (JSON), at | index(entity, entity_id) |

Check constraints: qty > 0, price >= 0, `remaining >= 0` (enforced in service plus DB check).

## 4. API Architecture

- Base: `/api/v1`. Auth: `POST /auth/login` returns JWT. Roles checked by a dependency (`require_admin`).
- Standard response: `{ "data": ..., "meta": { "page", "page_size", "total" }, "error": null }`.
- Errors: `{ "data": null, "error": { "code": "INSUFFICIENT_STOCK", "message": "..." } }`.
- List endpoints: `?page=&page_size=&search=&date_from=&date_to=&customer_id=&supplier_id=&batch_id=&status=&sale_type=`.

Endpoints (as in your prompt, plus):
`/dashboard`, `/suppliers`, `/customers`, `/customers/{id}/ledger`, `/purchases`, `/batches`, `/inventory`, `/inventory/adjustments`, `/sales`, `/sales/pos`, `/wastage`, `/payments`, `/expenses`, `/transports`, `/deliveries`, `/routes`, `/daily-closing` (open/close/reopen), `/reports/*` (with `?format=csv|xlsx|pdf`), `/settings`, `/users`, `/audit-logs`.

## 5. Frontend Page Map

Mobile: bottom nav (Dashboard, Sales, Stock, Wastage, More). Desktop: sidebar with all 12 items.

- Dashboard (8 KPI cards, 4 charts, alerts)
- Purchases (list, new purchase form with egg/petti/tray entry)
- Inventory (batch table, aging badges, variance panel)
- Sales (list, **POS quick screen**: qty x rate, CASH/UPI/CREDIT)
- Customers (list, detail, ledger)
- Suppliers (list, detail, payables)
- Transport (list, new shipment)
- Wastage (quick entry: batch, qty, reason)
- Payments (customer in, supplier out)
- Expenses
- Daily Operations (open day, live totals, close day)
- Reports (15 reports, export buttons)
- Settings, Users, Audit Log (admin only)

## 6. Folder Structure

As you proposed, with these additions:
```
backend/app/services/   purchase_service.py, landed_cost.py, inventory_service.py,
                        sales_service.py, wastage_service.py, ledger_service.py,
                        closing_service.py, reports_service.py
backend/tests/          one test file per service
frontend/src/features/  purchases/, sales/, wastage/ ...  (page + form + hooks together)
docs/                   architecture.md, er-diagram.md, backup.md, assumptions.md
```

## 7. Phase Plan

Same 10 phases as your prompt. Each phase ends with: tests passing, run instructions, your OK before the next phase. Phase 1 = repo, Docker (Postgres, backend, frontend), Alembic, login, base layout, health check.

## 8. Key Business Rules (how I will implement them)

1. **Landed cost per egg** = (egg cost + allocated transport + loading + unloading + packing + other) / sellable eggs. Recalculated when transport is attached or damage is recorded.
2. **Sell/FEFO**: sale picks oldest batch first; one sale can span batches. Staff can override with a warning.
3. **COGS** uses the cost snapshot stored on each sale item, so later cost changes never rewrite past profit.
4. **Stock** = sum of inventory_txns per batch. Sale and wastage fail if the result would go below 0.
5. **Customer outstanding** = ledger running balance, updated in the same database transaction as the sale or payment.
6. **Profit** = revenue - COGS - operating expenses. Cash collected is shown separately and never called profit.
7. **Daily closing**: expected = opening + purchases - sales - wastage (+/- adjustments). Non-zero variance requires a reason and creates a W6 adjustment. Closed days are locked; only ADMIN can reopen (logged).
8. Everything important goes to the audit log.

## 9. Edge Cases to Handle

- Sale spanning two batches; sale edited or cancelled after payment (reverses inventory and ledger).
- Payment larger than invoice (advance, stored as customer credit).
- Transport entered after the purchase (landed cost recalculated; sold eggs keep their old snapshot or get corrected? see question 1).
- One shipment carrying eggs from two suppliers.
- Damage on arrival recorded late.
- Customer return (restock vs wastage).
- Backdated entries into a closed day.
- Two staff selling the last eggs at the same time (row locking).
- Rounding: 30,000 x 0.3333 transport share; remainder is added to the last batch so totals match exactly.
- Soft-deleted records excluded from all totals but kept in the audit trail.

## 10. Development Environment Setup

Needed: Docker Desktop, Git, Node 20+, Python 3.12+ (optional if using Docker only).
```
git clone <repo> && cd egg-business
cp .env.example .env        # set DB password and JWT secret
docker compose up --build   # Postgres + backend (8000) + frontend (5173)
```
Backend docs at `http://localhost:8000/docs`. Migrations: `docker compose exec backend alembic upgrade head`. Tests: `docker compose exec backend pytest`.
Phone testing: open `http://<your-PC-IP>:5173` on the same Wi-Fi.

---

## NEEDS CLARIFICATION (I will not guess these)

See the chat message for the questions with lettered options.
