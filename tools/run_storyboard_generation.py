import json
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from agents.storyboard_agent import StoryboardAgent

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
    print("\nStarting Storyboard Generation Agent...\n")

    input_file = get_latest_file("scripts_*.json")
    print(f"Reading latest scripts: {input_file.name}\n")

    data = load_json(input_file)
    scripts = data.get("scripts", [])

    if not scripts:
        raise ValueError(f"No 'scripts' found in {input_file.name}")

    context_file = BASE_DIR / "data" / "product" / "crowdwisdom_context.json"
    product_context = load_json(context_file) if context_file.exists() else None

    agent = StoryboardAgent()
    print(f"Generating detailed storyboards for {len(scripts)} scripts...\n")

    storyboards = agent.create_storyboards(
        scripts=scripts,
        product_context=product_context
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"storyboards_{timestamp}.json"

    output_data = {
        "generated_at": datetime.now().isoformat(),
        "brand": "CrowdWisdomTrading",
        "source_scripts": input_file.name,
        "storyboards": {
            "storyboards": storyboards
        }
    }

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(output_data, file, indent=4, ensure_ascii=False)

    print("Storyboard Generation Complete!")
    print(f"Total storyboards generated: {len(storyboards)}")
    print(f"Saved to:\n{output_file}\n")


if __name__ == "__main__":
    main()
