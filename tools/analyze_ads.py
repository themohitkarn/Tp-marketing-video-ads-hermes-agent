import json
from pathlib import Path
from datetime import datetime
import sys


BASE_DIR = Path(
    __file__
).resolve().parent.parent

sys.path.append(
    str(BASE_DIR)
)

from agents.ad_analysis_agent import (
    AdAnalysisAgent
)


PROCESSED_DIR = (
    BASE_DIR / "outputs"
)


def get_latest_processed_file():

    files = list(
        PROCESSED_DIR.glob(
            "processed_ads_*.json"
        )
    )

    if not files:

        raise FileNotFoundError(
            "No processed ads file found."
        )

    return max(
        files,
        key=lambda file: (
            file.stat().st_mtime
        )
    )


def main():

    print(
        "\nStarting Hermes Ad Analysis...\n"
    )

    input_file = (
        get_latest_processed_file()
    )

    print(
        f"Reading: {input_file.name}"
    )

    agent = AdAnalysisAgent(
        input_file
    )

    results = (
        agent.run_analysis()
    )

    output_data = {

        "analysis_time":
        datetime.now().isoformat(),

        "source_file":
        input_file.name,

        "total_ads":
        len(results),

        "analysis":
        results
    }

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = (
        PROCESSED_DIR /
        f"ad_analysis_{timestamp}.json"
    )

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
        "\nAnalysis completed successfully!"
    )

    print(
        f"Ads analyzed: {len(results)}"
    )

    print(
        f"Output saved: {output_file}"
    )


if __name__ == "__main__":
    main()