# Plan: lowest price on MacBook Air M5 13" / 512GB, Thanksgiving 2026

Thanksgiving is **Thu Nov 26, 2026**. Black Friday is Nov 27 and Cyber Monday is Nov 30.

## 1. Lock the exact SKU (so you compare like for like)

MacBook Air 13" **M5, 16GB RAM, 512GB SSD**, in any color you'd accept.
Allowing every color matters: retailers often discount only one or two colors.

Price reference points (as of mid-2026 reports):

| | Price |
|---|---|
| Apple list price | $1,099 (some outlets list $1,299, see note) |
| All-time low (Amazon, late May 2026) | **$899.99** |
| Typical sale price (Jun–Jul 2026) | $949 – $1,149 |

Sources disagree on the list price, so check apple.com before you rely on it.

**Targets:**
- **Buy instantly:** $900 or less, effective price before tax.
- **Good deal:** $949 or less.
- **Walk away / wait for Cyber Monday:** over $999.

## 2. Watch these retailers

| Retailer | Notes |
|---|---|
| Amazon | Usually the price leader on M-series Airs. Turn on a CamelCamelCamel alert. |
| Best Buy | Usually matches Amazon. My Best Buy members sometimes get an extra $50–100 off. |
| Costco | Includes 2 years of AppleCare and an extended return window. Members only. |
| Walmart | Sometimes has doorbusters. Watch for "sold by Walmart", not marketplace sellers. |
| Micro Center | In-store pricing is often lower. Has student discounts. |
| B&H / Adorama | Tax-free for some states with B&H Payboo card. |
| Apple Store | Rarely discounts. Black Friday usually means a gift card (~$100) instead. Apple Refurbished is ~15% off all year. |
| Apple Education | Use it if you qualify (student, teacher, parent of student). Usually ~$100 off, plus a gift card during the Back-to-School promo. |

## 3. Set up alerts (do it this week)

1. **CamelCamelCamel** (Amazon): set a price-drop alert at $900.
2. **Slickdeals**: create a Deal Alert for the keywords `MacBook Air M5 512`.
3. **Honey / Keepa / Google Shopping price tracking**: set a target price on the listing.
4. **Retailer apps**: save the item to your wishlist on Best Buy, Walmart and Target. They send price-drop pushes.
5. **Deal sites (check daily)**: MacRumors deals, AppleInsider price guide, 9to5Toys, iClarified.

## 4. Stack savings to get the *effective* price

Effective price = sale price + sales tax − gift card or credit − card cash back − portal cash back.

- **Cash-back portals**: Rakuten, TopCashback, Capital One Shopping. Electronics usually pay 1–5%.
- **Credit card**: pick the card with the best electronics rate, purchase protection and extended warranty. Amex and many Visa Signature cards add one more year of warranty.
- **Discounted gift cards**: Costco or Sam's sells Best Buy and Apple gift cards at a discount. Some cards earn 5x at office stores on gift cards.
- **Apple gift-card promo**: count it as about 80–90% of face value, since you have to spend it at Apple.
- **Trade-in**: compare Apple, Best Buy and Amazon trade-in offers for your old laptop.

Run `python3 deal_tracker.py` to compare offers on the effective price, not the sticker price.

## 5. Timeline

| When | Action |
|---|---|
| Nov 11–16 | Set up all alerts. Record a baseline price at every retailer (`deal_tracker.py add`). |
| Nov 17–25 | "Early Black Friday" sales begin. Buy at $899 or less, since the price-protection and return windows cover you. |
| **Nov 26 (Thu)** | Most online deals go live the night before. Check Amazon, Best Buy and Walmart at 9pm ET on Wed Nov 25. |
| Nov 27 (Fri) | Doorbusters. Check Apple's gift-card promo and Costco in-store. |
| Nov 30 (Mon) | Cyber Monday. Amazon often re-drops prices. Last chance at the low. |
| Dec 1 – Jan | Holiday return windows. If the price drops further, use price-match or return and rebuy. |

## 6. Protect yourself after buying

- **Price-match / price protection**: Best Buy price-matches its own lower price during the return window. Amazon doesn't, but you can return the item and rebuy.
- **Holiday return windows**: most retailers extend returns to mid-January for purchases made in Nov–Dec. Keep checking until then.
- **Seller check**: buy only items "sold by" the retailer itself (Amazon.com, Best Buy). Avoid third-party marketplace sellers with suspiciously low prices.
- **Model check**: confirm the chip is **M5** and the storage is 512GB in the listing title *and* the spec sheet. Older M4 models get discounted heavily and can be confused for it.

## 7. Using the tracker

```bash
cd macbook_deal
python3 deal_tracker.py add --store Amazon --price 949 --cashback 2 --card 2
python3 deal_tracker.py add --store Apple --price 1099 --gift-card 100 --card 3   # gift card counted at 85%
python3 deal_tracker.py add --store "B&H" --price 979 --tax -8.25 --note "Payboo, tax-free"  # model a tax saving as negative
python3 deal_tracker.py best      # cheapest current offer + BUY / GOOD / WAIT verdict
python3 deal_tracker.py list      # latest offer per store, ranked by effective price
python3 deal_tracker.py history amazon
```

Targets are before tax because tax is the same at most stores. To credit a store that refunds tax (B&H Payboo, for example), enter that tax as a negative `--tax`.
Offers are saved to `macbook_deal/offers.csv`.
