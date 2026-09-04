import json
from pathlib import Path
from datetime import datetime


class AdAnalysisAgent:
    """
    Analyzes processed Meta ads and extracts
    marketing patterns and useful insights.
    """

    def __init__(self, input_file):
        self.input_file = Path(input_file)

    def load_ads(self):
        """Load processed ads JSON."""

        with open(
            self.input_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data.get("ads", [])

    def analyze_ad(self, ad):
        """Analyze one advertisement."""

        body = ad.get("body") or ""
        caption = ad.get("caption") or ""
        title = ad.get("title") or ""
        cta = ad.get("cta_text") or ""

        full_text = " ".join([
            body,
            caption,
            title
        ]).lower()

        insights = {
            "ad_id": ad.get("ad_id"),

            "page_name": ad.get("page_name"),

            "title": title,

            "cta": cta,

            "has_video": len(
                ad.get("videos", [])
            ) > 0,

            "copy_length": len(
                full_text
            ),

            "hook": self.extract_hook(
                body,
                caption,
                title
            ),

            "marketing_angles": self.detect_angles(
                full_text
            ),

            "emotional_triggers": self.detect_triggers(
                full_text
            ),

            "cta_strength": self.evaluate_cta(
                cta
            ),
        }

        return insights

    def extract_hook(
        self,
        body,
        caption,
        title
    ):
        """
        Uses the first meaningful text
        as the initial hook.
        """

        for text in [
            body,
            caption,
            title
        ]:

            if text:

                sentence = text.split(".")[0]

                return sentence[:200]

        return None

    def detect_angles(self, text):

        angles = []

        keywords = {

            "education": [
                "learn",
                "training",
                "course",
                "education",
                "mentor",
                "webinar"
            ],

            "money": [
                "money",
                "income",
                "profit",
                "earn",
                "financial"
            ],

            "urgency": [
                "now",
                "today",
                "limited",
                "hurry",
                "last chance"
            ],

            "social_proof": [
                "thousands",
                "customers",
                "students",
                "trusted",
                "people"
            ],

            "problem_solution": [
                "problem",
                "struggle",
                "solution",
                "improve",
                "help"
            ],

            "free_offer": [
                "free",
                "no cost",
                "without paying"
            ]
        }

        for angle, words in keywords.items():

            for word in words:

                if word in text:

                    angles.append(angle)

                    break

        return angles

    def detect_triggers(self, text):

        triggers = []

        trigger_keywords = {

            "fear": [
                "risk",
                "loss",
                "mistake",
                "danger"
            ],

            "greed": [
                "profit",
                "earn",
                "money",
                "income"
            ],

            "curiosity": [
                "secret",
                "discover",
                "hidden",
                "how"
            ],

            "trust": [
                "trusted",
                "expert",
                "mentor",
                "proven"
            ],

            "aspiration": [
                "success",
                "freedom",
                "improve",
                "lifestyle"
            ]
        }

        for trigger, words in (
            trigger_keywords.items()
        ):

            for word in words:

                if word in text:

                    triggers.append(
                        trigger
                    )

                    break

        return triggers

    def evaluate_cta(self, cta):

        if not cta:
            return "none"

        strong_ctas = [
            "sign up",
            "shop now",
            "learn more",
            "get offer",
            "download",
            "subscribe"
        ]

        if cta.lower() in strong_ctas:
            return "strong"

        return "moderate"

    def run_analysis(self):

        ads = self.load_ads()

        print(
            f"\nAnalyzing {len(ads)} ads...\n"
        )

        analysis_results = []

        for ad in ads:

            result = self.analyze_ad(ad)

            analysis_results.append(
                result
            )

        return analysis_results
    def save_results(self, results, output_file):

        output_file = Path(output_file)

        output_data = {

            "generated_at":
                datetime.now().isoformat(),

            "total_ads_analyzed":
                len(results),

            "analysis":
                results
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
            f"\nAnalysis saved to:\n"
            f"{output_file}"
        )    