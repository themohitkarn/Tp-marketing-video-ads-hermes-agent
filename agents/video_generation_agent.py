import os
import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class VideoGenerationAgent:
    def __init__(self, input_file):
        
        self.input_file = input_file
        api_key = os.getenv(
            "OPENROUTER_API_KEY"
            )
        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not found in .env file"
                )
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        self.model = "openrouter/free"
    
    def load_prompt(self):
        with open(
            self.input_file,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        video_prompts = data.get(
            "video_prompts",
            []
        )

        return video_prompts
    def process_prompts(self):

        video_prompts = self.load_prompt()

        print(
            f"Total video prompts: "
            f"{len(video_prompts)}\n"
        )

        for video_prompt in video_prompts:

            ad_number = video_prompt.get(
                "ad_number"
            )

            scene_number = video_prompt.get(
                "scene_number"
            )

            generated_prompt = video_prompt.get(
                "generated_video_prompt"
            )

            print(
                f"Ad {ad_number} | "
                f"Scene {scene_number}"
            )

            print(
                f"Video Prompt:\n"
                f"{generated_prompt}\n"
            )