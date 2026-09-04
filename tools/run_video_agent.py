import sys
import json

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from datetime import datetime
from pathlib import Path


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


sys.path.append(
    str(BASE_DIR)
)


from agents.video_agent import VideoAgent


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
        "\nStarting Video Agent...\n"
    )

    storyboard_file = get_latest_file(
        "storyboards_*.json"
    )

    print(
        f"Storyboard file: "
        f"{storyboard_file.name}\n"
    )

    agent = VideoAgent(
        storyboard_file
    )

    print(
        "Processing storyboards...\n"
    )

    video_prompts = (
        agent.process_storyboards()
    )

    timestamp = (
        datetime.now()
        .strftime(
            "%Y%m%d_%H%M%S"
        )
    )

    output_file = (
        OUTPUT_DIR /
        f"video_prompts_{timestamp}.json"
    )

    output_data = {

        "generated_at":
            datetime.now().isoformat(),

        "source_storyboard":
            storyboard_file.name,

        "total_video_prompts":
            len(video_prompts),

        "video_prompts":
            video_prompts
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
        "\nVideo Agent processing completed!"
    )

    print(
        f"\nTotal video prompts: "
        f"{len(video_prompts)}"
    )

    print(
        f"\nSaved to:\n"
        f"{output_file}"
    )


if __name__ == "__main__":
    main()