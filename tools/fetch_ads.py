import os
import json
from datetime import datetime
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")

if not APIFY_API_TOKEN:
    raise ValueError("APIFY_API_TOKEN not found in .env file")


ACTOR_ID = "unseenuser/meta-ads"

client = ApifyClient(APIFY_API_TOKEN)


def fetch_ads():
    print("\nStarting Meta Ads collection...\n")

    # Exact input taken from successful Apify run
    run_input = {
        "adType": "all",

        "countries": [
            "ALL"
        ],

        "enrichment": False,
        "getTranscript": False,

        # We will do AI analysis ourselves using OpenRouter
        "llmAnalysis": False,

        "longRunningDays": 30,

        "maxItems": 20,
        "maxItemsPerTerm": 5,
        "maxPagesPerQuery": 1,

        "platform": "ALL",

        "searchMode": "search_ads",

        "searchTerms": [
            "forex trading",
            "stock trading",
            "investment",
            "trading signals"
        ],

        "searchType": "keyword_unordered",

        "sortBy": "total_impressions",

        "startDate": "2026-08-05",

        "status": "ACTIVE",

        "strategySummary": False,
        "thumbnail": False,

        "languages": []
    }

    print("Calling Apify actor...")

    run = client.actor(ACTOR_ID).call(
        run_input=run_input
    )

    print("Actor run completed!")

    # Apify client may return either a dict or Pydantic model
    dataset_id = (
        run.get("defaultDatasetId")
        if isinstance(run, dict)
        else run.default_dataset_id
    )

    print("Dataset ID:", dataset_id)

    ads = []

    print("Fetching ads from dataset...")

    for item in client.dataset(dataset_id).iterate_items():
        ads.append(item)

    print(f"Total ads collected: {len(ads)}")

    # Create data directory
    os.makedirs("data/raw", exist_ok=True)

    filename = (
        "data/raw/"
        f"ads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            ads,
            file,
            ensure_ascii=False,
            indent=2,
            default=str
        )

    print("\nSUCCESS!")
    print(f"Ads saved to: {filename}")

    return ads


if __name__ == "__main__":
    fetch_ads()