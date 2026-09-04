import json
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from agents.ad_script_agent import AdScriptAgent

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
    print("\nStarting Ad Script Generation Agent...\n")

    input_file = get_latest_file("ad_concepts_*.json")
    print(f"Reading latest ad concepts: {input_file.name}\n")

    data = load_json(input_file)
    concepts = data.get("ad_concepts")

    if not concepts:
        raise ValueError(f"No 'ad_concepts' found in {input_file.name}")

    context_file = BASE_DIR / "data" / "product" / "crowdwisdom_context.json"
    product_context = load_json(context_file) if context_file.exists() else None

    agent = AdScriptAgent()
    print(f"Generating video scripts for {len(concepts)} concepts...\n")

    scripts = agent.generate_scripts(
        concepts=concepts,
        product_context=product_context
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"scripts_{timestamp}.json"

    output_data = {
        "generated_at": datetime.now().isoformat(),
        "source_concepts": input_file.name,
        "brand": "CrowdWisdomTrading",
        "total_scripts": len(scripts),
        "scripts": scripts
    }

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(output_data, file, indent=4, ensure_ascii=False)

    print("Ad Script Generation Complete!")
    print(f"Total scripts generated: {len(scripts)}")
    print(f"Saved to:\n{output_file}\n")


if __name__ == "__main__":
    main()
