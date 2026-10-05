# pip install apify-client
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("datagrit/app-release-review-impact").call(run_input={
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
})
items = client.dataset(run["defaultDatasetId"]).list_items().items
print(len(items), "records")
print(items[0] if items else None)
