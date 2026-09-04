import sys
import json

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


from agents.video_generation_agent import VideoGenerationAgent


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
        "\nStarting Video Generation Agent...\n"
    )

    video_prompts_file = get_latest_file(
        "video_prompts_*.json"
    )

    print(
        f"Video prompts file: "
        f"{video_prompts_file.name}\n"
    )
    
    agent = VideoGenerationAgent(
        video_prompts_file
    )
    
    print(
        "Processing video prompts...\n"
    )
    agent.process_prompts()
    
    print(
        "\nVideo Generation Agent "
        "processing completed!"
    )
    


if __name__ == "__main__":
    main()