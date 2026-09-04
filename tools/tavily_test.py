import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

if not api_key:
    raise ValueError("TAVILY_API_KEY not found in .env file")

tavily = TavilyClient(api_key=api_key)

response = tavily.search(
    query="What are the biggest problems retail traders face?",
    search_depth="basic",
    max_results=3,
)

print("\nTAVILY RESULTS:\n")

for i, result in enumerate(response["results"], start=1):
    print(f"{i}. {result['title']}")
    print(result["url"])
    print()