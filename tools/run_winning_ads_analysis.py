import json
import sys

from pathlib import Path
from datetime import datetime


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


sys.path.append(
    str(BASE_DIR)
)


from agents.winning_ads_agent import (
    WinningAdsAgent
)


OUTPUT_DIR = (
    BASE_DIR / "outputs"
)


def get_latest_ad_analysis():

    files = list(
        OUTPUT_DIR.glob(
            "ad_analysis_*.json"
        )
    )

    if not files:

        raise FileNotFoundError(
            "Ad analysis file not found."
        )

    return max(
        files,
        key=lambda file:
            file.stat().st_mtime
    )


def main():

    print(
        "\nStarting Winning Ads Analysis...\n"
    )

    input_file = (
        get_latest_ad_analysis()
    )

    print(
        f"Reading: "
        f"{input_file.name}\n"
    )

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)


    results = data.get(
        "analysis",
        []
    )


    if not results:

        raise ValueError(
            "No ad analysis results found."
        )


    print(
        f"Analyzing patterns from "
        f"{len(results)} ads...\n"
    )


    agent = WinningAdsAgent()


    insights = (
        agent.analyze_patterns(
            results
        )
    )


    timestamp = (
        datetime.now()
        .strftime(
            "%Y%m%d_%H%M%S"
        )
    )


    output_file = (
        OUTPUT_DIR /
        f"marketing_insights_{timestamp}.json"
    )


    output_data = {

        "generated_at":
            datetime.now().isoformat(),

        "source_file":
            input_file.name,

        "total_ads_analyzed":
            len(results),

        "marketing_insights":
            insights
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


    print(
        "\nWinning Ads Analysis Complete!"
    )

    print(
        f"\nTotal ads analyzed: "
        f"{len(results)}"
    )

    print(
        f"\nInsights saved to:\n"
        f"{output_file}"
    )


if __name__ == "__main__":
    main()