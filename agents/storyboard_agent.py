import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class StoryboardAgent:
    """
    StoryboardAgent transforms structured ad scripts into fully realized
    visual storyboards containing granular scene timings, visual cues,
    voiceover lines, text overlays, emotions, and strategic purposes,
    specifically formatted for downstream cinematic prompt generation.
    """

    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")

        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in .env file")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

        self.model = "openrouter/free"

    def create_storyboards(self, scripts, product_context=None):
        """
        Converts scripts into detailed scene-by-scene storyboards.
        """
        prompt = f"""
You are an elite video creative director and storyboard producer.
Your task is to transform these video scripts into detailed, production-ready storyboards for CrowdWisdomTrading.

SCRIPTS:
{json.dumps(scripts, indent=2)}

BRAND CONTEXT:
{json.dumps(product_context, indent=2) if product_context else "Brand: CrowdWisdomTrading. Trading intelligence and collective market insights."}

STRICT COMPLIANCE RULES:
1. Do not promise profits or guaranteed returns.
2. Ensure each scene is clearly visualized without making fraudulent claims.
3. Keep visual pacing dynamic and suitable for short-form video ads (30-60 seconds total per ad).

For each script, create a storyboard with 5 to 8 detailed scenes.
Each scene MUST include:
- scene_number (integer starting from 1)
- duration_seconds (integer, typically 3 to 10 seconds)
- visual (detailed cinematic description of what is seen on screen)
- voiceover (exact spoken words for this scene)
- text_overlay (concise, punchy on-screen text graphics)
- emotion (e.g., Frustration, Curiosity, Relief, Empowerment, Anticipation)
- purpose (e.g., "Pattern interrupt hook", "Deepen pain point", "Introduce solution", "Social proof", "Direct CTA")

Return ONLY valid JSON matching this exact structure:
{{
    "storyboards": [
        {{
            "ad_number": 1,
            "ad_type": "",
            "title": "",
            "target_icp": "",
            "duration_seconds": 45,
            "core_pain_point": "",
            "marketing_angle": "",
            "visual_hook": "",
            "voiceover_hook": "",
            "cta": "",
            "scenes": [
                {{
                    "scene_number": 1,
                    "duration_seconds": 3,
                    "visual": "",
                    "voiceover": "",
                    "text_overlay": "",
                    "emotion": "",
                    "purpose": ""
                }}
            ]
        }}
    ]
}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert storyboard producer. "
                        "Return only valid JSON without markdown fences or additional commentary."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        content = response.choices[0].message.content.strip()

        if content.startswith("```json"):
            content = content[len("```json"):]
        elif content.startswith("```"):
            content = content[len("```"):]

        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Failed to parse LLM response as JSON: {exc}\nResponse content: {content}")

        storyboard_list = parsed.get("storyboards", [])
        if not storyboard_list and isinstance(parsed, list):
            storyboard_list = parsed

        if not storyboard_list:
            raise ValueError("No storyboards found in the LLM response.")

        return storyboard_list
