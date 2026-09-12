import json
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_latest_json_file():
    """Get the latest raw ads JSON file."""

    files = list(RAW_DIR.glob("ads_*.json"))

    if not files:
        raise FileNotFoundError(
            "No ads JSON file found in data/raw/"
        )

    return max(files, key=lambda file: file.stat().st_mtime)


def clean_ad(ad):
    """Extract useful fields from a raw Meta ad."""

    snapshot = ad.get("snapshot", {})

    videos = snapshot.get("videos", [])

    video_data = []

    for video in videos:
        video_data.append({
            "video_hd_url": video.get("video_hd_url"),
            "video_sd_url": video.get("video_sd_url"),
            "video_preview_image_url": video.get(
                "video_preview_image_url"
            ),
        })

    return {
        "ad_id": ad.get("ad_archive_id"),

        "page_name": ad.get("page_name"),

        "page_profile_url": snapshot.get(
            "page_profile_uri"
        ),

        "is_active": ad.get("is_active"),

        "caption": snapshot.get("caption"),

        "body": snapshot.get("body", {}).get(
            "text"
        ),

        "title": snapshot.get("title"),

        "cta_text": snapshot.get("cta_text"),

        "cta_type": snapshot.get("cta_type"),

        "link_url": snapshot.get("link_url"),

        "display_format": snapshot.get(
            "display_format"
        ),

        "videos": video_data,

        "platforms": ad.get(
            "publisher_platform"
        ),

        "start_date": ad.get(
            "start_date_string"
        ),

        "end_date": ad.get(
            "end_date_string"
        ),

        "categories": ad.get(
            "page_categories"
        ),

        "raw_source": "meta_ad_library"
    }


def main():

    print("\nStarting ads processing...\n")

    input_file = get_latest_json_file()

    print(f"Reading file: {input_file.name}")

    with open(input_file, "r", encoding="utf-8") as file:
        raw_ads = json.load(file)

    print(f"Raw ads found: {len(raw_ads)}")

    processed_ads = []

    for ad in raw_ads:

        try:
            cleaned_ad = clean_ad(ad)
            processed_ads.append(cleaned_ad)

        except Exception as error:

            print(
                f"Skipping ad due to error: {error}"
            )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = (
        OUTPUT_DIR /
        f"processed_ads_{timestamp}.json"
    )

    output_data = {
        "processed_at": datetime.now().isoformat(),
        "source_file": input_file.name,
        "total_ads": len(processed_ads),
        "ads": processed_ads
    }

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nProcessing completed successfully!")

    print(
        f"Processed ads: {len(processed_ads)}"
    )

    print(
        f"Output saved to: {output_file}"
    )


if __name__ == "__main__":
    main()