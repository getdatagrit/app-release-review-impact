# App Release Review Impact: Rating by Version

Groups App Store and Google Play reviews by app version and shows how each release changed the rating, with significance flags and the complaints that are new in that version.

[![Run on Apify](https://img.shields.io/badge/Run%20on-Apify-0f9f74)](https://apify.com/datagrit/app-release-review-impact) [![Docs](https://img.shields.io/badge/docs-getdatagrit.github.io-0e1726)](https://getdatagrit.github.io/app-release-review-impact/)

**from $2.80 per 1,000 results + $10 per run (pay per result; the rate depends on your Apify plan).** Export as JSON, CSV or Excel, call it through the API, or schedule it on Apify.

## What it does

App Release Review Impact reads the newest public reviews of Apple App Store and Google Play apps and groups them by app version. For every version you get the review count, the average rating, the star distribution, how the rating changed against the previous version, whether that change is statistically significant, and the complaint terms that are new in that release. It is built for product managers, QA and support leads, app store optimization teams and analysts who want to know which release made users unhappy without reading thousands of reviews.

Review scrapers return one row per review with a raw version string. This Actor returns one row per version, so a regression shows up as a single line with a trend of `regressed` instead of a spreadsheet pivot you have to build yourself.

## Quick start

1. Open [App Release Review Impact: Rating by Version on Apify Store](https://apify.com/datagrit/app-release-review-impact) and click **Try for free**.
2. Fill in the input form (or paste the JSON below) and run it.
3. Download the dataset, or fetch it from the API.

```json
{
  "apps": [
    "com.spotify.music",
    "com.reddit.frontpage",
    "com.whatsapp",
    "com.instagram.android",
    "com.netflix.mediaclient",
    "com.duolingo"
  ],
  "countries": [
    "us"
  ],
  "maxReviewsPerApp": 500,
  "minReviewsPerVersion": 10,
  "maxItems": 200
}
```

## Input

| Field | Type | What it does |
|---|---|---|
| `apps` (required) | array | App Store IDs (digits, e.g. 1064216828), apps.apple.com URLs, Google Play package names (e.g. com.reddit.frontpage) or play.google.com URLs. Mix both stores freely; every app is analyzed separately within its own store. |
| `countries` | array | Two-letter App Store storefronts to read for App Store apps (us, gb, de, ...; uk is read as gb). A code the App Store does not know is reported and skipped. Reviews of all selected countries are merged into one row per version. The App Store feed exposes at most the 500 newest reviews per country and often only the first 50. Google Play apps ignore this field. |
| `googlePlayCountry` | string | Two-letter Google Play country used when reading Google Play apps. |
| `googlePlayLanguage` | string | Language code of the Google Play page (en, de, pt-br, ...). It sets the language of the interface, not a filter on review language. |
| `maxReviewsPerApp` | integer | Newest reviews to read per app. For App Store apps this limit applies per country; the feed pages 50 reviews at a time up to 500 and often stops after the first page. Google Play allows up to 5000, and more reviews reach further back in version history there; the strict newComplaintTerms list fills mainly at 2000 to 5000. |
| `minReviewsPerVersion` | integer | Versions with fewer reviews are left out, because averages over a handful of reviews are noise. Rating changes are always compared with the nearest older version that passes this limit. |
| `latestVersions` | integer | Keep only the N newest versions of each app that pass the minimum reviews limit. Zero keeps all of them. |
| `onlyRegressions` | boolean | Return only versions whose average rating dropped by at least 0.15 stars against the previous version and the drop is statistically significant (95 % confidence). |
| `maxItems` | integer | Stop after this many version rows in total across all apps. |
| `proxyConfiguration` | object | Apify Proxy is on by default. The App Store review feed sometimes answers with an empty page; the Actor retries an empty first page up to six times, gives every app a budget of at most 75 seconds for everything that goes wrong (pauses after empty pages, waits before retrying HTTP 429 or server errors and the time spent in attempts that failed; each attempt is also cut off after 25 seconds), limited to an equal share of the 150 seconds of the whole run and never below 9 seconds so that apps that were not touched yet can still be read, and gives an app it cannot read within its budget a free status row. If the proxy cannot be created the run continues without it. |

## Output

| Field | Type | Description |
|---|---|---|
| `store` | string | Store the app and its reviews come from: app-store or google-play. |
| `appId` | string | App Store numeric ID or Google Play package name as given in the input. |
| `appName` | string | Name of the app on the store page. Empty only on the status row of an app that was not found, or whose store lookup did not answer. |
| `version` | string | App version string exactly as reported with the reviews. |
| `versionRank` | integer | Position among the versions kept for this app, 1 = newest version. |
| `reviewCount` | integer | Number of reviews written on this version within the reviews that were read. |
| `avgRating` | number | Mean star rating of the reviews on this version, rounded to two decimals. |
| `stars1Count` | integer | Number of 1-star reviews on this version. |
| `stars2Count` | integer | Number of 2-star reviews on this version. |
| `stars3Count` | integer | Number of 3-star reviews on this version. |
| `stars4Count` | integer | Number of 4-star reviews on this version. |
| `stars5Count` | integer | Number of 5-star reviews on this version. |
| `lowStarCount` | integer | Number of reviews with one or two stars on this version. |
| `lowStarShare` | number | Share of reviews on this version that have one or two stars, from 0 to 1. |
| `firstReviewAt` | string | ISO 8601 time of the oldest review on this version within the reviews that were read. |
| `lastReviewAt` | string | ISO 8601 time of the newest review on this version within the reviews that were read. |
| `previousVersion` | string | Nearest older version of the same app that passes the minimum reviews limit. Empty for the oldest version. |
| `previousAvgRating` | number | Mean star rating of the previous version. |
| `ratingDelta` | number | Average rating of this version minus that of the previous version, in stars. Empty for the oldest version. |
| `ratingDeltaMargin` | number | Half-width of the 95 % confidence interval of the rating change, in stars (plus or minus). A change smaller than this margin cannot be told from chance. Empty for the oldest version. |
| `previousLowStarShare` | number | Share of 1-2 star reviews on the previous version, from 0 to 1. |
| `lowStarShareDelta` | number | Share of 1-2 star reviews on this version minus that of the previous version. |
| `deltaSignificant` | boolean | True when the rating change is statistically significant at 95 % confidence (Welch t test on the star ratings), false when it is not. Empty for the oldest version. |
| `trend` | string | regressed or improved when the rating changed by at least 0.15 stars and the change is significant. stable when the change is under 0.15 stars and the 95 % margin is at most 0.3 stars. inconclusive when the sample is too small to tell (a visible change that is not significant, or a margin wider than 0.3 stars): read ratingDelta together with ratingDeltaMargin. baseline for the oldest version that has no predecessor. |
| `newComplaintTerms` | array | Words and two-word phrases that are significantly more frequent in the 1-2 star reviews of this version than in the 1-2 star reviews of all older versions (one-sided two-proportion test, z of at least 3, at least 3 % of the version's low-star reviews, at least twice the older frequency, at least 4 reviews). Empty array: the comparison was made and no term stands out. Null: no comparison is possible (oldest version, or fewer than 12 low-star reviews in the version or in the older versions together), which is the usual case with 500 reviews per app; it fills mainly on Google Play reads of 5000 reviews. See newComplaintTermStats for the numbers and lowStarTopTerms for the most frequent low-star terms of every version. |
| `newComplaintTermStats` | array | For each term in newComplaintTerms: lowStarReviews (1-2 star reviews of this version containing it), versionShare (their share of the version's 1-2 star reviews), olderShare (the same share in the older versions) and lift (versionShare divided by olderShare, the older share never taken below 1 % or below one review of the older pool). Null when newComplaintTerms is null. |
| `lowStarTopTerms` | array | The five most frequent words and phrases in the 1-2 star reviews of this version, new or not, with the same numbers as newComplaintTermStats (olderShare and lift are null for the oldest version and whenever all older versions together hold fewer than 12 low-star reviews; lift is the version share divided by the older share, which is never taken below 1 % or below one review of the older pool). Where a lift exists, a value near 1 means the term is about as frequent as before and a high value that it is more frequent in this release. Null when the version has fewer than 8 low-star reviews; an empty array when it has 8 or more but no word or phrase occurs in at least 4 of them. |
| `lowStarTopTermsText` | string | The same five terms as lowStarTopTerms as one readable string, with the lift against older versions in brackets where one exists (for example "log (lift 11.1), working (lift 4.2), login"). Null when lowStarTopTerms is null or empty. This is the column of the Version impact view. |
| `sampleLowStarReviews` | array | Up to three 1-2 star review texts from this version, preferring those that contain the new complaint terms, then the most helpful, cut at 280 characters. No author names. |
| `countries` | array | Storefront countries whose reviews were merged into this row (App Store), or the Google Play country that was read. On a status row of an app that could not be read: the storefronts that were looked up. |
| `sourceUrl` | string | Store page of the app. Also on the status row of an app that could not be read, whenever the store lookup answered. |
| `scrapedAt` | string | ISO 8601 timestamp of the run. |
| `found` | boolean | False only on status rows, which explain why an app produced no version rows. Status rows are not billed. |
| `note` | string | Reason for a status row. On a version row it is empty, or it warns that part of the requested reviews was not served by the store or that only some of the reviews carry an app version (counted per storefront; a storefront below the threshold, 20 % for Google Play and 90 % for the App Store, is named as left out of the statistics). |

Sample record:

```json
{
  "store": "app-store",
  "appId": "1064216828",
  "appName": "Reddit",
  "version": "2026.38.0",
  "versionRank": 2,
  "reviewCount": 108,
  "avgRating": 1.93,
  "stars1Count": 70,
  "stars2Count": 9,
  "stars3Count": 6,
  "stars4Count": 4,
  "stars5Count": 19,
  "lowStarCount": 79,
  "lowStarShare": 0.731,
  "firstReviewAt": "2026-09-22T14:03:11.000Z",
  "lastReviewAt": "2026-09-26T21:40:02.000Z",
  "previousVersion": "2026.37.0",
  "previousAvgRating": 1.9,
  "ratingDelta": 0.03,
  "ratingDeltaMargin": 0.27,
  "previousLowStarShare": 0.712,
  "lowStarShareDelta": 0.019,
  "deltaSignificant": false,
  "trend": "inconclusive",
  "newComplaintTerms": [
    "login",
    "crash on startup"
  ],
  "newComplaintTermStats": [
    {
      "term": "login",
      "lowStarReviews": 104,
      "versionShare": 0.15,
      "olderShare": 0.022,
      "lift": 6.5
    }
  ],
  "lowStarTopTerms": [
    {
      "term": "account",
      "lowStarReviews": 103,
      "versionShare": 0.149,
      "olderShare": 0.039,
      "lift": 3.8
    }
  ],
  "lowStarTopTermsText": "account (lift 3.8), login, update",
  "sampleLowStarReviews": [
    "App crashes on startup since the last update."
  ],
  "countries": [
    "us"
  ],
  "sourceUrl": "https://apps.apple.com/us/app/id1064216828",
  "scrapedAt": "2026-10-01T08:00:00.000Z",
  "found": true,
  "note": "No app version has at least 10 reviews (read 120 reviews across 14 versions). Lower minReviewsPerVersion or raise maxReviewsPerApp."
}
```

## Call it from code

Runnable examples are in [`examples/`](examples). Replace `YOUR_APIFY_TOKEN` with the token from your Apify account settings.

```bash
curl -X POST "https://api.apify.com/v2/acts/datagrit~app-release-review-impact/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"apps":["com.spotify.music","com.reddit.frontpage","com.whatsapp","com.instagram.android","com.netflix.mediaclient","com.duolingo"],"countries":["us"],"maxReviewsPerApp":500,"minReviewsPerVersion":10,"maxItems":200}'
```

## FAQ

**Is it legal to scrape app store reviews?**  
The Actor reads public review data from the same public endpoints the stores use for their own pages and the App Store review feed. It collects no data behind a login and does not store reviewer names.

**How many reviews can I get?**  
Up to 5000 per Google Play app. The App Store feed allows up to 500 per country, but it often serves only the first 50, so add countries or run again for more.

**How often should I run it?**  
Weekly or after each release. A scheduled run shows the newest version as soon as it has enough reviews.

**Why is a version missing?**  
It has fewer reviews than the minimum, or it is older than the reviews that the store made available in this run.

**Why is a visible drop not marked regressed?**  
Then the trend is `inconclusive`: with this few reviews the drop cannot be told from chance (see `ratingDeltaMargin`). `stable` is used only when the change is under 0.15 stars and the sample is large enough to rule out a bigger one.

**Something looks wrong in the data.**  
Open an issue on the Actor page with the input you used and the run link.

## More from datagrit

- [TED Contract Expiry Radar - Recompete Leads](https://github.com/getdatagrit/ted-contract-expiry-radar) - Find EU public contracts approaching expiry from TED award notices: incumbent, buyer, value, end date and renewal options.
- [UK Contract Expiry Radar - Recompete Leads](https://github.com/getdatagrit/uk-contract-expiry-radar) - UK public contracts ending soon with incumbent supplier, buyer, value and contact - recompete leads from Contracts Finder award notices.
- [French Company Finder - Sirene Financials](https://github.com/getdatagrit/french-company-finder) - French company lead lists from Sirene screened by net result and revenue, with net margin, size, matching establishment and optional directors.
- [IRS 990 Nonprofit Officers and Compensation](https://github.com/getdatagrit/irs-990-officer-compensation) - Named officers, directors and key employees with pay, hours and titles from IRS e-filed 990, 990-EZ and 990-PF returns.
- [Poland KRS New Company Registrations Feed](https://github.com/getdatagrit/poland-krs-new-companies) - Newly registered Polish companies, foundations and associations from the official KRS court register: NIP, address, PKD, capital, email, with filters and change detection.

All Actors: [https://getdatagrit.github.io/](https://getdatagrit.github.io/) · [Apify Store](https://apify.com/datagrit)

---

This repository holds documentation and usage examples. Questions, bug reports and feature requests: use the **Issues** tab of the Actor page on [Apify Store](https://apify.com/datagrit/app-release-review-impact). Examples are MIT licensed.
