import os
import json
from datetime import datetime, timedelta

from dotenv import load_dotenv
from tavily import TavilyClient


load_dotenv()


class ResearchAgent:
    """
    Researches recent ICP and pain-point information
    using Tavily.
    """

    def __init__(self):

        api_key = os.getenv("TAVILY_API_KEY")

        if not api_key:
            raise ValueError(
                "TAVILY_API_KEY not found in .env file"
            )

        self.client = TavilyClient(
            api_key=api_key
        )

    def search(self, query, max_results=5):

        print(f"\nSearching: {query}")

        response = self.client.search(
            query=query,
            search_depth="basic",
            max_results=max_results
        )

        return response.get(
            "results",
            []
        )

    def research_trader_pain_points(self):

        queries = [
            "retail traders biggest challenges pain points 2026",
            "retail trading problems losses emotions FOMO 2026",
            "retail investors information overload market research 2026",
            "trading psychology challenges fear greed discipline 2026",
            "why retail traders struggle to make trading decisions 2026"
        ]

        research = {}

        for query in queries:

            results = self.search(query)

            research[query] = results

        return research


def main():

    agent = ResearchAgent()

    research_results = (
        agent.research_trader_pain_points()
    )

    output = {
        "generated_at":
            datetime.now().isoformat(),

        "research_period":
            "recent market and trader research",

        "research":
            research_results
    }

    return output


if __name__ == "__main__":

    data = main()

    print(
        "\nResearch completed successfully!"
    )

    print(
        json.dumps(
            data,
            indent=2
        )
    )   