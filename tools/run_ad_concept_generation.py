import json
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from agents.ad_concept_agent import AdConceptAgent

OUTPUT_DIR = BASE_DIR / "outputs"


def get_latest_file(pattern):
    files = list(OUTPUT_DIR.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No file found matching pattern: {pattern}")
    return max(files, key=lambda f: f.stat().st_mtime)


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    print("\nStarting Ad Concept Generation Agent...\n")

    input_file = get_latest_file("marketing_insights_*.json")
    print(f"Reading latest marketing insights: {input_file.name}\n")

    data = load_json(input_file)
    insights = data.get("marketing_insights")

    if not insights:
        raise ValueError(f"No 'marketing_insights' key found in {input_file.name}")

    context_file = BASE_DIR / "data" / "product" / "crowdwisdom_context.json"
    product_context = load_json(context_file) if context_file.exists() else None

    agent = AdConceptAgent()
    print("Generating original ad concepts from marketing insights...\n")

    concepts = agent.generate_ad_concepts(
        marketing_insights=insights,
        product_context=product_context
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"ad_concepts_{timestamp}.json"

    output_data = {
        "generated_at": datetime.now().isoformat(),
        "source_file": input_file.name,
        "brand": "CrowdWisdomTrading",
        "total_concepts": len(concepts),
        "ad_concepts": concepts
    }

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(output_data, file, indent=4, ensure_ascii=False)

    print("Ad Concept Generation Complete!")
    print(f"Total concepts generated: {len(concepts)}")
    print(f"Saved to:\n{output_file}\n")


if __name__ == "__main__":
    main()
