# Sample: compare attribution models

Run on WorkMagic's demo store (a Shopify test shop with synthetic orders, Oct 12–29, 2026).
The reply is abridged; your assistant's wording will differ.

---

**You:** Compare Meta and Google attributed revenue under data-driven, last click, first click and
any-click attribution for the last 30 days, and explain why they differ.

**Assistant:**

| Channel | Model | Attributed orders | Attributed revenue |
|---|---|---|---|
| Meta | Data-driven | 11.8 | $10.2K |
| Meta | Last click | 19 | $17.3K |
| Meta | First click | 30 | $27.1K |
| Meta | Any click | 41 | $38.0K |
| Google | Data-driven | 13.7 | $12.7K |
| Google | Last click | 22 | $19.9K |
| Google | Any click | 37 | $33.2K |

What's going on:

- **Meta opens journeys, Google closes them.** Meta's first-click credit ($27.1K) is far above its
  last-click credit ($17.3K): shoppers discover the store through Meta, then return through Google
  search or direct traffic to buy.
- **Data-driven attribution shares credit.** It splits each order across every touchpoint, so both
  channels get less than under any single-touch model. Fractional orders (11.8) are the result.
- **Any-click double counts by design.** Every channel that touched an order gets full credit, so
  Meta and Google together ($71.2K) exceed what the store actually sold ($46.9K). Use it to see reach,
  not to add up revenue.

*Source: all sales platforms, Oct 12–29, 2026.*
