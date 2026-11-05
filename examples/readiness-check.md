# Sample: measurement readiness check

Run on WorkMagic's demo store (a Shopify test shop with synthetic orders, Oct 12–29, 2026).
The reply is abridged; your assistant's wording will differ.

---

**You:** Is my WorkMagic account ready for attribution, media mix modeling and lift tests? What do I
need to fix first?

**Assistant:**

| Product | Status | What's in the way |
|---|---|---|
| Attribution (MTA) | Was ready, now has gaps | Orders, checkout pixel and page-view pixel all have gaps in the past 45 days; Meta ad spend is missing |
| Media mix modeling (MBO) | Not ready | Needs a completed lift test and calibrated attribution on at least one ad platform |
| Lift tests | Not ready on the sales side | Under 180 days of order history, under 3,600 orders in the past 30 days, and more than 30% of orders from one region |

Fix first: **reconnect Meta ad spend and check the pixel.** Attribution is the only product that was
ready before, and it needs continuous orders, pixel events and spend to stay accurate. Lift tests and
MMM need months of order history, so they'll follow once data has been flowing for a while.
