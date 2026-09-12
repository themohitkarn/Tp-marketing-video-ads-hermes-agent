import argparse
import json
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
OPENMONTAGE_DIR = Path(r"D:\OpenMontage")


def get_latest_file(pattern):
    files = list(OUTPUT_DIR.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No file found: {pattern}")
    return max(files, key=lambda file: file.stat().st_mtime)


def build_cinematic_movie_ad_props(brand="cwt"):
    """
    Constructs a true cinematic, movie-style video advertisement with full audio
    (neural AI voiceover narration + cinematic background music).

    Supports:
      brand="cwt"        -> CrowdWisdomTrading (for CEO Gilad assessment submission)
      brand="tradepulse" -> TradePulse AI (for public LinkedIn portfolio)
    """
    if brand.lower() == "tradepulse":
        brand_title = "TradePulse AI"
        brand_sub = "Stop Guessing. Start Knowing. Explore Free at tradepulse.ai"
        narration_file = "narration_tradepulse.mp3"
    else:
        brand_title = "CrowdWisdomTrading"
        brand_sub = "Stop Guessing. Start Knowing. Explore Free at crowdwisdomtrading.com"
        narration_file = "narration_cwt.mp3"

    cuts = [
        {
            "id": "movie-scene-1-hook",
            "source": "footage/scene_1_hook_trader.mp4",
            "source_in_seconds": 1.0,
            "in_seconds": 0.0,
            "out_seconds": 6.0,
            "transition_in": "fade",
            "transition_out": "fade",
            "transition_duration": 0.5,
            "backgroundColor": "#0A0F1D"
        },

        {
            "id": "movie-scene-2-overload",
            "source": "footage/scene_2_phone_overload.mp4",
            "source_in_seconds": 0.5,
            "in_seconds": 6.0,
            "out_seconds": 12.0,
            "transition_in": "fade",
            "transition_out": "fade",
            "transition_duration": 0.5,
            "backgroundColor": "#0A0F1D"
        },

        {
            "id": "movie-scene-3-volatility",
            "source": "footage/scene_3_candlestick_volatility.mp4",
            "source_in_seconds": 1.0,
            "in_seconds": 12.0,
            "out_seconds": 18.0,
            "transition_in": "fade",
            "transition_out": "fade",
            "transition_duration": 0.5,
            "backgroundColor": "#0A0F1D"
        },

        {
            "id": "movie-scene-4-convergence",
            "source": "footage/tech_data_flow.mp4",
            "source_in_seconds": 0.0,
            "in_seconds": 18.0,
            "out_seconds": 24.5,
            "transition_in": "fade",
            "transition_out": "fade",
            "transition_duration": 0.5,
            "backgroundColor": "#0A0F1D"
        },

        {
            "id": "movie-scene-5-dashboard",
            "source": "footage/scene_4_financial_screen.mp4",
            "source_in_seconds": 1.0,
            "in_seconds": 24.5,
            "out_seconds": 31.0,
            "transition_in": "fade",
            "transition_out": "fade",
            "transition_duration": 0.5,
            "backgroundColor": "#0A0F1D"
        },

        {
            "id": "movie-scene-6-confident",
            "source": "footage/scene_5_confident_trader.mp4",
            "source_in_seconds": 0.5,
            "in_seconds": 31.0,
            "out_seconds": 37.0,
            "transition_in": "fade",
            "transition_out": "fade",
            "transition_duration": 0.5,
            "backgroundColor": "#0A0F1D"
        },

        {
            "id": "movie-scene-7-wallstreet",
            "source": "footage/scene_6_wall_street_nyse.mp4",
            "source_in_seconds": 0.5,
            "in_seconds": 37.0,
            "out_seconds": 42.0,
            "transition_in": "fade",
            "transition_out": "fade",
            "transition_duration": 0.5,
            "backgroundColor": "#0A0F1D"
        },

        {
            "id": "movie-scene-8-cta",
            "source": "",
            "type": "hero_title",
            "in_seconds": 42.0,
            "out_seconds": 48.0,
            "text": brand_title,
            "subtitle": brand_sub,
            "accentColor": "#38BDF8",
            "backgroundColor": "#0A0F1D"
        }
    ]

    overlays = [
        {
            "type": "section_title",
            "in_seconds": 0.5,
            "out_seconds": 5.5,
            "text": "VOLATILE MARKETS",
            "subtitle": "Are you catching the moves — or getting caught in the noise?",
            "accentColor": "#EF4444",
            "position": "top-left"
        },

        {
            "type": "section_title",
            "in_seconds": 6.5,
            "out_seconds": 11.5,
            "text": "15 TABS. 50 TELEGRAM ALERTS.",
            "subtitle": "Endless notifications, zero high-conviction clarity",
            "accentColor": "#F59E0B",
            "position": "top-left"
        },

        {
            "type": "stat_reveal",
            "in_seconds": 12.5,
            "out_seconds": 17.5,
            "text": "CANDLESTICK NOISE",
            "subtitle": "Solo guesswork entering late and burning capital",
            "accentColor": "#EF4444",
            "position": "bottom-right"
        },

        {
            "type": "section_title",
            "in_seconds": 18.5,
            "out_seconds": 24.0,
            "text": "COLLECTIVE INTELLIGENCE",
            "subtitle": "50,000+ trader perspectives unified into real-time consensus",
            "accentColor": "#38BDF8",
            "position": "top-left"
        },

        {
            "type": "stat_reveal",
            "in_seconds": 25.0,
            "out_seconds": 30.5,
            "text": "1 UNIFIED HUB",
            "subtitle": "Sentiment bias, key levels & aggregated signals in one place",
            "accentColor": "#10B981",
            "position": "bottom-right"
        },

        {
            "type": "section_title",
            "in_seconds": 31.5,
            "out_seconds": 36.5,
            "text": "STRUCTURED CONFIDENCE",
            "subtitle": "From anxiety and hesitation to decisive execution",
            "accentColor": "#10B981",
            "position": "top-left"
        },

        {
            "type": "stat_reveal",
            "in_seconds": 37.5,
            "out_seconds": 41.5,
            "text": "WALL STREET EDGE",
            "subtitle": "Institutional-grade perspective in retail hands",
            "accentColor": "#38BDF8",
            "position": "bottom-right"
        }
    ]

    return {
        "theme": "flat-motion-graphics",
        "cuts": cuts,
        "overlays": overlays,
        "captions": [],
        "audio": {
            "narration": {
                "src": f"audio/{narration_file}",
                "volume": 1.0
            },
            "music": {
                "src": "audio/background_music.mp3",
                "volume": 0.15,
                "loop": True,
                "fadeInSeconds": 1.5,
                "fadeOutSeconds": 2.5
            }
        }
    }


def main():
    parser = argparse.ArgumentParser(description="Generate OpenMontage Props with Audio")
    parser.add_argument("--brand", choices=["cwt", "tradepulse"], default="cwt",
                        help="Brand to target ('cwt' for CrowdWisdomTrading, 'tradepulse' for TradePulse AI)")
    args = parser.parse_args()

    print("\n========================================================")
    print(f"Generating Cinematic Movie Video Ad Props [Brand: {args.brand.upper()}]...")
    print("========================================================\n")

    video_prompt_file = get_latest_file("video_prompts_*.json")
    print(f"Referencing latest cinematic video prompts: {video_prompt_file.name}")

    props_data = build_cinematic_movie_ad_props(brand=args.brand)

    output_file = OUTPUT_DIR / f"{args.brand}_openmontage_props.json"
    crowdwisdom_output = OUTPUT_DIR / "crowdwisdom_openmontage_props.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(props_data, file, indent=2, ensure_ascii=False)

    shutil.copy(output_file, crowdwisdom_output)

    print(f"Generated {len(props_data['cuts'])} cinematic scenes / cuts.")
    print(f"Generated {len(props_data['overlays'])} narrative title & stat overlays.")
    print(f"Audio configured: Narration ({props_data['audio']['narration']['src']}) + Background Music ({props_data['audio']['music']['src']}).")
    print("Total runtime: 48 seconds.")
    print(f"Saved props to: {output_file}\n")

    destination = (
        OPENMONTAGE_DIR /
        "remotion-composer" /
        "public" /
        "demo-props" /
        "crowdwisdom.json"
    )

    shutil.copy(output_file, destination)
    print(f"Synced to OpenMontage demo props:\n{destination}\n")


if __name__ == "__main__":
    main()
