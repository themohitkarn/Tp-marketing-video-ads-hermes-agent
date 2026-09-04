import json
from pathlib import Path
from datetime import datetime
import sys


BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR))


from agents.ai_ad_agent import AIAdAgent


OUTPUT_DIR = BASE_DIR / "outputs"


def get_latest_processed_file():

    files = list(
        OUTPUT_DIR.glob(
            "processed_ads_*.json"
        )
    )

    if not files:
        raise FileNotFoundError(
            "Processed ads file not found."
        )

    return max(
        files,
        key=lambda file: file.stat().st_mtime
    )


def main():

    print(
        "\nStarting AI Ad Analysis...\n"
    )

    input_file = get_latest_processed_file()

    print(
        f"Reading: {input_file.name}"
    )

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    ads = data.get("ads", [])

    print(
        f"Total ads to analyze: {len(ads)}\n"
    )

    agent = AIAdAgent()

    results = []

    for index, ad in enumerate(
        ads,
        start=1
    ):

        print(
            f"Analyzing ad "
            f"{index}/{len(ads)}..."
        )

        try:

            analysis = agent.analyze_ad(ad)

            results.append({
                "ad": ad,
                "ai_analysis": analysis
            })

        except Exception as error:

            print(
                f"Error analyzing ad "
                f"{index}: {error}"
            )

            results.append({
                "ad": ad,
                "ai_analysis": {
                    "error": str(error)
                }
            })

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = (
        OUTPUT_DIR /
        f"ai_ad_analysis_{timestamp}.json"
    )

    output_data = {

        "generated_at":
        datetime.now().isoformat(),

        "source_file":
        input_file.name,

        "total_ads":
        len(results),

        "results":
        results
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

    print("\nAI Analysis Completed!")

    print(
        f"Output saved to:\n"
        f"{output_file}"
    )


if __name__ == "__main__":
    main()