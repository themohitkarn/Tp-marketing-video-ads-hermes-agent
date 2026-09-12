import os
import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class AIAdAgent:
    """
    Uses an LLM to analyze successful ads and extract
    marketing pain points, hooks, concepts and patterns.
    """

    def __init__(self):

        api_key = os.getenv("OPENROUTER_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not found in .env file"
            )

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

        self.model = "openrouter/free"

    def analyze_ad(self, ad):

        ad_data = {
            "page_name": ad.get("page_name"),
            "title": ad.get("title"),
            "body": ad.get("body"),
            "caption": ad.get("caption"),
            "cta_text": ad.get("cta_text"),
            "start_date": ad.get("start_date"),
            "has_video": len(ad.get("videos", [])) > 0,
        }

        prompt = f"""
You are a senior performance marketing strategist.

Analyze this Meta advertisement from the
trading/investing niche.

AD DATA:
{json.dumps(ad_data, indent=2)}

Return ONLY valid JSON.

Use this structure:

{{
    "target_audience": "",
    "main_pain_points": [],
    "main_desires": [],
    "primary_hook": "",
    "hook_type": "",
    "marketing_angle": "",
    "emotional_triggers": [],
    "copywriting_patterns": [],
    "cta_strategy": "",
    "why_this_ad_may_work": "",
    "video_ad_concept": ""
}}

Focus on extracting reusable marketing insights
that can help create a high-performing video ad
for CrowdWisdomTrading.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert performance "
                        "marketing analyst. Always return "
                        "valid JSON only."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
        )

        content = response.choices[0].message.content

        content = content.strip()

        if content.startswith("```json"):
            content = content.replace(
                "```json",
                "",
                1
            )

        if content.startswith("```"):
            content = content.replace(
                "```",
                "",
                1
            )

        if content.endswith("```"):
            content = content[:-3]

        try:
            return json.loads(content.strip())

        except json.JSONDecodeError:

            return {
                "analysis_error": True,
                "raw_response": content
            }