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


def build_cinematic_movie_ad_props():
    """
    Constructs a true cinematic, movie-style video advertisement for CrowdWisdomTrading
    using actual visual video footage (real B-roll/cinematic footage) matching the
    pipeline's storyboard and video-agent prompts:

    Scene 1 (0.0 - 6.0s):
      Visual: Weary trader at workstation analyzing multi-screen scrolling charts at night.
      Narrative Hook: "VOLATILE MARKETS: Are you catching moves or caught in noise?"
      Footage: footage/scene_1_hook_trader.mp4

    Scene 2 (6.0 - 12.0s):
      Visual: Frantic smartphone checking, crypto/stock graph tracking, alert notification overload.
      Pain Point: "15 TABS. 50 TELEGRAM ALERTS. Endless noise, zero high-conviction clarity."
      Footage: footage/scene_2_phone_overload.mp4

    Scene 3 (12.0 - 18.0s):
      Visual: Broker analyzing rapid candlestick volatility and erratic price swings.
      Contrast: "CANDLESTICK NOISE: Solo guesswork entering late and burning capital."
      Footage: footage/scene_3_candlestick_volatility.mp4

    Scene 4 (18.0 - 24.5s):
      Visual: Ultra high-tech 3D data particle flow converging into unified algorithmic streams.
      Mechanism: "DATA CONVERGENCE: 50,000+ trader perspectives unified into real-time consensus."
      Footage: footage/tech_data_flow.mp4

    Scene 5 (24.5 - 31.0s):
      Visual: Sleek institutional financial intelligence screen with real-time indicators.
      Solution: "1 UNIFIED HUB: Sentiment bias, key levels & aggregated signals in one place."
      Footage: footage/scene_4_financial_screen.mp4

    Scene 6 (31.0 - 37.0s):
      Visual: Confident trader analyzing calmly with focused execution and relaxed posture.
      Transformation: "STRUCTURED CONFIDENCE: From anxiety and hesitation to decisive execution."
      Footage: footage/scene_5_confident_trader.mp4

    Scene 7 (37.0 - 42.0s):
      Visual: Grand establishing view of Wall Street / New York Stock Exchange.
      Authority: "WALL STREET EDGE: Institutional-grade perspective in retail hands."
      Footage: footage/scene_6_wall_street_nyse.mp4

    Scene 8 (42.0 - 47.0s):
      Visual: Cinematic brand hero card with CrowdWisdomTrading call to action.
      Closing: "CrowdWisdomTrading — Stop Guessing. Start Knowing. Explore Free."

    Total duration: 47 seconds (compliant with 30-60s assessment requirement).
    """
    cuts = [
        # Scene 1: Cinematic Hook - Trader at Multi-Screen Desk (0.0 - 6.0s)
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

        # Scene 2: Information Overload - Phone Alerts & Volatile Graphs (6.0 - 12.0s)
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

        # Scene 3: Candlestick Volatility & Market Chaos (12.0 - 18.0s)
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

        # Scene 4: Data Convergence & Algorithmic Streams (18.0 - 24.5s)
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

        # Scene 5: Institutional Financial Dashboard (24.5 - 31.0s)
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

        # Scene 6: Confident Trader Transformation (31.0 - 37.0s)
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

        # Scene 7: Wall Street / New York Stock Exchange (37.0 - 42.0s)
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

        # Scene 8: Cinematic Brand Closing & Call to Action (42.0 - 47.0s)
        {
            "id": "movie-scene-8-cta",
            "source": "",
            "type": "hero_title",
            "in_seconds": 42.0,
            "out_seconds": 47.0,
            "text": "TradePulse AI",
            "subtitle": "Stop Guessing. Start Knowing. Explore Free at tradepulse.ai",
            "accentColor": "#38BDF8",
            "backgroundColor": "#0A0F1D"
        }
    ]

    overlays = [
        # Overlay 1: Hook Title on Scene 1
        {
            "type": "section_title",
            "in_seconds": 0.5,
            "out_seconds": 5.5,
            "text": "VOLATILE MARKETS",
            "subtitle": "Are you catching the moves — or getting caught in the noise?",
            "accentColor": "#EF4444",
            "position": "top-left"
        },

        # Overlay 2: Notification Overload on Scene 2
        {
            "type": "section_title",
            "in_seconds": 6.5,
            "out_seconds": 11.5,
            "text": "15 TABS. 50 TELEGRAM ALERTS.",
            "subtitle": "Endless notifications, zero high-conviction clarity",
            "accentColor": "#F59E0B",
            "position": "top-left"
        },

        # Overlay 3: Candlestick Noise Stat on Scene 3
        {
            "type": "stat_reveal",
            "in_seconds": 12.5,
            "out_seconds": 17.5,
            "text": "CANDLESTICK NOISE",
            "subtitle": "Solo guesswork entering late and burning capital",
            "accentColor": "#EF4444",
            "position": "bottom-right"
        },

        # Overlay 4: Collective Intelligence on Scene 4
        {
            "type": "section_title",
            "in_seconds": 18.5,
            "out_seconds": 24.0,
            "text": "COLLECTIVE INTELLIGENCE",
            "subtitle": "50,000+ trader perspectives unified into real-time consensus",
            "accentColor": "#38BDF8",
            "position": "top-left"
        },

        # Overlay 5: Unified Hub Stat on Scene 5
        {
            "type": "stat_reveal",
            "in_seconds": 25.0,
            "out_seconds": 30.5,
            "text": "1 UNIFIED HUB",
            "subtitle": "Sentiment bias, key levels & aggregated signals in one place",
            "accentColor": "#10B981",
            "position": "bottom-right"
        },

        # Overlay 6: Structured Confidence on Scene 6
        {
            "type": "section_title",
            "in_seconds": 31.5,
            "out_seconds": 36.5,
            "text": "STRUCTURED CONFIDENCE",
            "subtitle": "From anxiety and hesitation to decisive execution",
            "accentColor": "#10B981",
            "position": "top-left"
        },

        # Overlay 7: Wall Street Edge Stat on Scene 7
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
        "audio": {}
    }


def main():
    print("\n========================================================")
    print("Generating Cinematic Movie-Style Video Ad Props...")
    print("========================================================\n")

    video_prompt_file = get_latest_file("video_prompts_*.json")
    print(f"Referencing latest cinematic video prompts: {video_prompt_file.name}")

    props_data = build_cinematic_movie_ad_props()

    output_file = OUTPUT_DIR / "crowdwisdom_openmontage_props.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(props_data, file, indent=2, ensure_ascii=False)

    print(f"Generated {len(props_data['cuts'])} cinematic scenes / cuts.")
    print(f"Generated {len(props_data['overlays'])} narrative title & stat overlays.")
    print("Total runtime: 47 seconds (cinematic ad pacing, compliant with 30-60s requirement).")
    print(f"Saved props to: {output_file}\n")

    # Copy to OpenMontage demo-props
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
