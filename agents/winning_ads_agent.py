import os
import json

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class WinningAdsAgent:

    def __init__(self):

        api_key = os.getenv(
            "OPENROUTER_API_KEY"
        )

        if not api_key:

            raise ValueError(
                "OPENROUTER_API_KEY not found"
            )

        self.client = OpenAI(

            base_url="https://openrouter.ai/api/v1",

            api_key=api_key
        )

        self.model = "openrouter/free"


    def analyze_patterns(
        self,
        ad_results
    ):

        simplified_ads = []

        for item in ad_results:

            simplified_ads.append({

                "ad_id":
                    item.get(
                        "ad_id"
                    ),

                "page_name":
                    item.get(
                        "page_name"
                    ),

                "title":
                    item.get(
                        "title"
                    ),

                "cta":
                    item.get(
                        "cta"
                    ),

                "has_video":
                    item.get(
                        "has_video"
                    ),

                "copy_length":
                    item.get(
                        "copy_length"
                    ),

                "hook":
                    item.get(
                        "hook"
                    ),

                "marketing_angles":
                    item.get(
                        "marketing_angles",
                        []
                    ),

                "emotional_triggers":
                    item.get(
                        "emotional_triggers",
                        []
                    ),

                "cta_strength":
                    item.get(
                        "cta_strength"
                    )
            })


        prompt = f"""
You are a senior performance marketing
strategist specializing in trading,
investing and fintech advertising.

You are given analysis data from
multiple Meta advertisements.

Your task is to identify the COMMON
WINNING MARKETING PATTERNS across
these advertisements.

ADS ANALYSIS:

{json.dumps(simplified_ads, indent=2)}

Return ONLY valid JSON.

Use this exact structure:

{{
    "market_summary": "",

    "ideal_customer_profile": {{
        "audience_description": "",
        "experience_level": "",
        "major_problems": [],
        "major_desires": [],
        "common_fears": []
    }},

    "top_pain_points": [],

    "top_desires": [],

    "winning_hooks": [
        {{
            "hook_pattern": "",
            "why_it_works": "",
            "example": ""
        }}
    ],

    "winning_marketing_angles": [
        {{
            "angle": "",
            "reason": ""
        }}
    ],

    "emotional_triggers": [],

    "winning_cta_patterns": [],

    "creative_patterns": [],

    "recommendations_for_crowdwisdomtrading": [
        ""
    ],

    "top_3_video_ad_concepts": [
        {{
            "concept_name": "",
            "hook": "",
            "problem": "",
            "solution_angle": "",
            "video_style": "",
            "cta": ""
        }}
    ]
}}

Focus only on patterns supported by
the provided advertisement data.

Focus on reusable marketing insights.

Do not invent claims about
CrowdWisdomTrading.

Do not provide financial advice.
"""


        response = (
            self.client.chat.completions.create(

                model=self.model,

                messages=[

                    {
                        "role": "system",

                        "content": (
                            "You are an expert "
                            "performance marketing "
                            "strategist. Analyze only "
                            "the provided data and "
                            "return only valid JSON."
                        )
                    },

                    {
                        "role": "user",

                        "content":
                            prompt
                    }
                ],

                temperature=0.7
            )
        )


        content = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )



        if content.startswith(
            "```json"
        ):

            content = (
                content[
                    len("```json"):
                ]
            )


        elif content.startswith(
            "```"
        ):

            content = (
                content[
                    len("```"):
                ]
            )


        if content.endswith(
            "```"
        ):

            content = content[:-3]


        return json.loads(
            content.strip()
        )