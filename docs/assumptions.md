# Assumptions and decisions

## Your decisions (from the approval step)
1. **Transport cost**: entered at purchase time. The system will not allow transport to be added after eggs are sold, so past sales never need recalculating.
2. **Profit (cost of sold eggs)**: uses the real landed cost of the batch each egg came from.
3. **Customer returns**: staff choose each time, put back in stock or record as wastage.
4. **Egg size**: one size per purchase batch.

## My assumptions (change any of these)
- You replied "Go" without letters, so I used the options I had recommended.
- One warehouse and one business for now. No `warehouse_id` or `business_id` columns yet.
- Phase 1 uses plain Tailwind. shadcn/ui is added when the first big forms need it (Phase 2).
- ESLint and Vitest are added in Phase 10 (testing phase). Prettier and TypeScript type-checking are set up now.
- Login token lasts 12 hours.
- Login response, errors and lists all use the same shape: `{ data, meta, error }`.
