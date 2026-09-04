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

from agents.script_agent import (
    ScriptAgent
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


def load_json(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def main():

    print(
        "\nStarting Script Agent...\n"
    )

    insights_file = get_latest_file(
        "marketing_insights_*.json"
    )

    research_file = get_latest_file(
        "market_research_*.json"
    )

    context_file = (
        BASE_DIR /
        "data" /
        "product" /
        "crowdwisdom_context.json"
    )

    print(
        f"Marketing insights: "
        f"{insights_file.name}"
    )

    print(
        f"Market research: "
        f"{research_file.name}"
    )

    marketing_data = load_json(
        insights_file
    )

    research_data = load_json(
        research_file
    )

    product_context = load_json(
        context_file
    )

    agent = ScriptAgent()

    print(
        "\nGenerating 3 video "
        "advertising storyboards...\n"
    )

    storyboards = (
        agent.create_storyboards(
            marketing_data,
            research_data,
            product_context
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
        f"storyboards_{timestamp}.json"
    )

    output_data = {

        "generated_at":
            datetime.now().isoformat(),

        "brand":
            "CrowdWisdomTrading",

        "storyboards":
            storyboards
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
        "\nStoryboards generated successfully!"
    )

    print(
        f"Saved to:\n{output_file}"
    )


if __name__ == "__main__":
    main()