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


from agents.ad_analysis_agent import (
    AdAnalysisAgent
)


OUTPUT_DIR = (
    BASE_DIR / "outputs"
)


def get_latest_file(pattern):

    files = list(
        OUTPUT_DIR.glob(pattern)
    )

    if not files:

        raise FileNotFoundError(
            f"No file found: {pattern}"
        )

    return max(
        files,
        key=lambda file:
            file.stat().st_mtime
    )


def main():

    print(
        "\nStarting Ad Analysis Agent...\n"
    )

    input_file = get_latest_file(
        "processed_ads_*.json"
    )

    print(
        f"Input file:\n"
        f"{input_file.name}\n"
    )

    agent = AdAnalysisAgent(
        input_file
    )

    results = agent.run_analysis()

    timestamp = (
        datetime.now()
        .strftime(
            "%Y%m%d_%H%M%S"
        )
    )

    output_file = (
        OUTPUT_DIR /
        f"ad_analysis_{timestamp}.json"
    )

    agent.save_results(
        results,
        output_file
    )

    print(
        "\nAd Analysis completed!"
    )

    print(
        f"\nTotal ads analyzed: "
        f"{len(results)}"
    )


if __name__ == "__main__":
    main()