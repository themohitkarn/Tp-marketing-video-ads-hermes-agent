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


from agents.research_agent import (
    ResearchAgent
)


OUTPUT_DIR = (
    BASE_DIR / "outputs"
)

OUTPUT_DIR.mkdir(
    exist_ok=True
)


def main():

    print(
        "\nStarting Tavily Market Research...\n"
    )

    agent = ResearchAgent()

    research = (
        agent.research_trader_pain_points()
    )

    timestamp = (
        datetime.now()
        .strftime(
            "%Y%m%d_%H%M%S"
        )
    )

    output_file = (
        OUTPUT_DIR /
        f"market_research_{timestamp}.json"
    )

    output_data = {

        "generated_at":
            datetime.now().isoformat(),

        "focus":
            "Retail trader ICP and pain point research",

        "source":
            "Tavily web search",

        "research":
            research
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
        "\nResearch completed!"
    )

    print(
        f"Results saved to:\n"
        f"{output_file}"
    )


if __name__ == "__main__":
    main()