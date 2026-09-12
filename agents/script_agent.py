import os
import json

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class ScriptAgent:

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

    def create_storyboards(
        self,
        marketing_insights,
        market_research,
        product_context
    ):

        prompt = f"""
You are an elite performance marketing
creative director and video ad scriptwriter.

Your task is to create THREE highly engaging
30–60 second video advertisements for
CrowdWisdomTrading.

You must use:

1. Winning competitor ad patterns
2. Recent retail trader pain-point research
3. ICP insights
4. Product context

MARKETING INSIGHTS:

{json.dumps(marketing_insights, indent=2)}

MARKET RESEARCH:

{json.dumps(market_research, indent=2)}

PRODUCT CONTEXT:

{json.dumps(product_context, indent=2)}

Create exactly 3 different ad types:

AD 1:
Pain-point driven

AD 2:
Data / insight driven

AD 3:
Transformation / before-after driven

Each ad must have:

- A powerful visual hook within the first 3 seconds
- A pattern interrupt
- Clear problem
- Emotional tension
- Product introduction
- Solution explanation
- Strong CTA

Return ONLY valid JSON.

Use this exact structure:

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

Create 6–10 scenes per advertisement.

The first 3 seconds must be visually powerful.

Do not promise profits.
Do not guarantee financial results.
Do not invent facts or statistics.
"""

        response = (
            self.client.chat.completions.create(
                model=self.model,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert video "
                            "advertising creative director. "
                            "Return valid JSON only."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.8
            )
        )

        content = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

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

        return json.loads(
            content.strip()
        )