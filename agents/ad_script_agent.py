import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class AdScriptAgent:
    """
    AdScriptAgent converts marketing ad concepts into fully developed,
    short-form (30-60s) video ad scripts with scene-by-scene narration,
    visual direction, and compliance guardrails.
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

    def generate_scripts(self, concepts, product_context=None):
        """
        Takes a list of ad concepts and generates detailed video ad scripts.
        """
        prompt = f"""
You are an expert performance video ad scriptwriter and creative director.
Your task is to take the provided ad concepts and develop a complete, high-converting video script for each concept for CrowdWisdomTrading.

AD CONCEPTS:
{json.dumps(concepts, indent=2)}

BRAND & PRODUCT GUIDELINES:
{json.dumps(product_context, indent=2) if product_context else "Brand: CrowdWisdomTrading. Trading intelligence and collective market insights platform."}

STRICT COMPLIANCE RULES:
1. Do NOT make financial guarantees, profit promises, or claims of risk-free trading.
2. Do NOT promise specific win rates or returns.
3. Keep the tone empowering, educational, and focused on clarity and reducing information overload.
4. Target duration: 30 to 60 seconds per video ad.

For each concept, write a structured video script with scene-by-scene narration, visual direction, on-screen text, and timing.

Return ONLY valid JSON matching this exact structure:
{{
    "scripts": [
        {{
            "concept_number": 1,
            "title": "",
            "hook": "",
            "estimated_duration": "45 seconds",
            "target_audience": "",
            "visual_intent": "",
            "cta": "",
            "scenes": [
                {{
                    "scene_number": 1,
                    "duration_seconds": 3,
                    "visual_direction": "",
                    "narration": "",
                    "on_screen_text": ""
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
                        "You are an elite video advertising scriptwriter. "
                        "Return only valid JSON without markdown fences or outside text."
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

        # Remove markdown code fences if present
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

        scripts = parsed.get("scripts", [])
        if not scripts and isinstance(parsed, list):
            scripts = parsed

        if not scripts:
            raise ValueError("No scripts were found in the LLM response.")

        return scripts
