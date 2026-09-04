import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class AdConceptAgent:
    """
    AdConceptAgent analyzes marketing insights and generates original,
    high-converting video ad concepts for CrowdWisdomTrading without making
    unsupported performance claims or financial guarantees.
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

    def generate_ad_concepts(self, marketing_insights, product_context=None):
        """
        Generates original ad concepts using marketing insights and product rules.
        """
        # Extract core marketing insights sections
        top_pain_points = marketing_insights.get("top_pain_points", [])
        top_desires = marketing_insights.get("top_desires", [])
        winning_hooks = marketing_insights.get("winning_hooks", [])
        winning_angles = marketing_insights.get("winning_marketing_angles", [])
        emotional_triggers = marketing_insights.get("emotional_triggers", [])
        cta_patterns = marketing_insights.get("winning_cta_patterns", [])
        recommendations = marketing_insights.get("recommendations_for_crowdwisdomtrading", [])
        preliminary_concepts = marketing_insights.get("top_3_video_ad_concepts", [])

        prompt = f"""
You are a senior creative strategist and performance marketing director.
Your task is to generate 3 to 5 original, high-performing video advertisement concepts for CrowdWisdomTrading.

MARKETING INSIGHTS DATA:
- Top Pain Points: {json.dumps(top_pain_points, indent=2)}
- Top Desires: {json.dumps(top_desires, indent=2)}
- Winning Hooks: {json.dumps(winning_hooks, indent=2)}
- Winning Marketing Angles: {json.dumps(winning_angles, indent=2)}
- Emotional Triggers: {json.dumps(emotional_triggers, indent=2)}
- Winning CTA Patterns: {json.dumps(cta_patterns, indent=2)}
- Recommendations for CrowdWisdomTrading: {json.dumps(recommendations, indent=2)}
- Preliminary Video Concepts: {json.dumps(preliminary_concepts, indent=2)}

BRAND & PRODUCT CONTEXT:
{json.dumps(product_context, indent=2) if product_context else "Brand: CrowdWisdomTrading. Trading intelligence and collective market insights platform."}

STRICT COMPLIANCE & CLAIM RULES:
1. Do not promise profits or trading success.
2. Do not guarantee financial returns or risk-free trading.
3. Do not invent fake statistics, user counts, or performance track records.
4. Position CrowdWisdomTrading around reducing information overload, structured intelligence, and smarter decision making.

Generate distinct concepts covering different strategic angles (e.g., Pain-Relief & Overwhelm, Data & Structured Intelligence, Community & Shared Perspectives).

Return ONLY valid JSON with this exact structure:
{{
    "concepts": [
        {{
            "concept_number": 1,
            "concept_name": "",
            "target_audience": "",
            "target_pain_point": "",
            "target_desire": "",
            "hook": "",
            "core_message": "",
            "marketing_angle": "",
            "emotional_trigger": "",
            "video_style": "",
            "cta": ""
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
                        "You are an expert creative marketing strategist. "
                        "Return only valid JSON without explanation or commentary."
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

        concepts = parsed.get("concepts", [])
        if not concepts and isinstance(parsed, list):
            concepts = parsed

        if not concepts:
            raise ValueError("No ad concepts were generated in the LLM response.")

        return concepts
