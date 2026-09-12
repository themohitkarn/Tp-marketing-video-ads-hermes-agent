import os
import sys
import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()


class VideoAgent:

    def __init__(self, input_file):

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

        self.input_file = input_file


    def load_storyboard(self):

        with open(
            self.input_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        storyboard_data = data.get(
            "storyboards",
            {}
        )

        if isinstance(storyboard_data, list):
            storyboards = storyboard_data
        elif isinstance(storyboard_data, dict):
            storyboards = storyboard_data.get(
                "storyboards",
                []
            )
        else:
            storyboards = []

        return storyboards


    def process_storyboards(self):
        

        storyboards = self.load_storyboard()
        video_prompts = []
        

        print(
            f"Total storyboards: "
            f"{len(storyboards)}\n"
        )

        for storyboard in storyboards:

            print(
                f"Ad {storyboard.get('ad_number')}: "
                f"{storyboard.get('title')}"
            )

            scenes = storyboard.get(
                "scenes",
                []
            )

            for scene in scenes:

                print(
                    f"Scene "
                    f"{scene.get('scene_number')}: "
                    f"{scene.get('visual')}"
                )
                

            
            
                video_prompt = self.generate_video_prompt(scene)
                video_prompts.append(
                    {
                        "ad_number": storyboard.get("ad_number"),
                        "scene_number": scene.get("scene_number"),
                        "original_visual": scene.get("visual"),
                        "generated_video_prompt": video_prompt
                    }
                )
                
                
                print(
                    "\nGenerated Video Prompt:"
                    )
                try:
                    print(video_prompt)
                except Exception:
                    print(video_prompt.encode("ascii", errors="replace").decode("ascii"))
        return video_prompts
                
            
    def generate_video_prompt(self, scene):
        
        visual = scene.get("visual")
        emotion = scene.get("emotion")
        duration = scene.get("duration_seconds")
        voiceover = scene.get("voiceover")
        text_overlay = scene.get("text_overlay")
        purpose = scene.get("purpose")
        
        prompt = f"""You are an expert AI video prompt engineer.
        Create a detailed cinematic video-generation prompt based on the following scene.
        Visual: {visual}
        Emotion: {emotion}
        Duration: {duration}
        Voiceover context: {voiceover}
        Text overlay: {text_overlay}
        Purpose: {purpose}
        Include:
        - subject and action
        - environment
        - camera angle and movement
        - lighting
        - mood and emotion
        - cinematic style
        - pacing appropriate for the duration

        Do not generate dialogue, captions, or text overlays inside the video.
        Return only the final video-generation prompt."""
    
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                    }
                ]
            )
        video_prompt = response.choices[0].message.content   
        return video_prompt
        