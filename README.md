# CrowdWisdomTrading AI Marketing Video Ads Agent (Hermes Framework)

Autonomous multi-agent marketing video creation pipeline developed for **CrowdWisdomTrading** as part of the Marketing AI Lead assessment.

The system orchestrates a fleet of specialized AI agents using the **Hermes Agent Framework** pattern, transforming raw Meta ad competitor data and real-time market intelligence into a broadcast-quality, 47-second motion-graphics video advertisement rendered via **OpenMontage (Remotion)**.

---

## 🎯 Project Overview & Scope

| Assessment Stage | Specialized Agent | Tool / Technology | Output Artifact |
|---|---|---|---|
| **1. Ads Mining** | `AdsManagerAgent` | Apify Meta Ads Scraper | `outputs/processed_ads_*.json` |
| **2. Ad Analysis** | `AdAnalysisAgent` | Rule-based feature extraction | `outputs/ad_analysis_*.json` |
| **3. Winning Ads Analysis** | `WinningAdsAgent` | OpenRouter (`openrouter/free`) | `outputs/marketing_insights_*.json` |
| **4. Pain & ICP Research** | `ResearchAgent` | Tavily Web Search API | `outputs/market_research_*.json` |
| **5. Ad Concept Ideation** | `AdConceptAgent` | OpenRouter LLM Strategy | `outputs/ad_concepts_*.json` |
| **6. Short-Form Scriptwriting**| `AdScriptAgent` | 30–60s Scriptwriting Agent | `outputs/scripts_*.json` |
| **7. Storyboard Production** | `StoryboardAgent` | Granular Scene Producer | `outputs/storyboards_*.json` |
| **8. Cinematic Video Prompts**| `VideoAgent` | Camera & Lighting Prompting | `outputs/video_prompts_*.json` |
| **9. Remotion Motion Props** | `OpenMontageProps`| Motion Graphics Generator | `crowdwisdom.json` |
| **10. Video Ad Rendering** | `OpenMontage Engine`| Remotion React / H.264 | `crowdwisdom.mp4` |

---

## 🚀 Quickstart & Setup

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- FFmpeg (installed and added to PATH)

### 2. Environment Configuration (`.env`)
Create a `.env` file in the project root containing your API credentials:
```env
OPENROUTER_API_KEY=your_openrouter_api_key
APIFY_API_TOKEN=your_apify_api_token
TAVILY_API_KEY=your_tavily_api_key
```

### 3. Virtual Environment Activation
```powershell
cd D:\CWT_Marketing_Video_Ads_Hermes_Agent
.\venv\Scripts\Activate.ps1
```

---

## ⚡ Execution Pipeline (Step-by-Step)

Each stage can be executed independently; runner scripts dynamically detect the latest timestamped output from the preceding stage:

```powershell
# 1. Process Scraped Meta Ads
python tools/process_ads.py

# 2. Extract Ad Hooks & Emotional Triggers
python tools/run_ad_analysis.py

# 3. Synthesize Winning Market Patterns
python tools/run_winning_ads_analysis.py

# 4. Generate 3 Strategic Ad Concepts
python tools/run_ad_concept_generation.py

# 5. Write 30-60s Short-Form Video Scripts
python tools/run_script_generation.py

# 6. Produce Granular Storyboards
python tools/run_storyboard_generation.py

# 7. Generate Cinematic Video Prompts
python tools/run_video_agent.py

# 8. Compile OpenMontage Remotion Motion-Graphics Props
python tools/create_openmontage_props.py

# 9. Render Final MP4 in OpenMontage
cd D:\OpenMontage
python render_demo.py crowdwisdom
cd D:\CWT_Marketing_Video_Ads_Hermes_Agent
```

The rendered video will be available at:
`D:\OpenMontage\projects\demos\renders\crowdwisdom.mp4`

---

## 📊 Live Hermes Kanban Board

To launch the real-time terminal Kanban board:
```powershell
python tools/hermes_kanban.py --live
```
This displays all 10 agent tasks transitioning across `[BACKLOG]`, `[IN PROGRESS]`, `[REVIEW]`, and `[DONE]` with deliverables and status metrics.

---

## 🎬 Cinematic Movie-Style Video Ad Structure (48 Seconds)

Adhering strictly to CEO Gilad's feedback (*"why the videos are not movie videos? why remotion style?"*), the pipeline combines the cinematic camera prompts from `VideoAgent` with real high-definition video footage composited seamlessly via OpenMontage:

1. **0.0s – 6.0s (The Hook)**: Real cinematic footage of a trader at night surrounded by glowing multi-monitor workstations scanning live candlestick charts (`scene_1_hook_trader.mp4`) with dynamic title overlay: *"VOLATILE MARKETS: Are you catching the moves — or getting caught in the noise?"*.
2. **6.0s – 12.0s (Information Overload)**: Real footage of a trader frantically tracking trade graphs and endless alerts on a smartphone (`scene_2_phone_overload.mp4`) with *"15 TABS. 50 TELEGRAM ALERTS: Endless notifications, zero high-conviction clarity"*.
3. **12.0s – 18.0s (Market Chaos)**: Real footage of a broker analyzing volatile candlestick movements in the dark (`scene_3_candlestick_volatility.mp4`) with *"CANDLESTICK NOISE: Solo guesswork entering late and burning capital"*.
4. **18.0s – 24.5s (Data Convergence)**: Ultra high-definition 3D cybernetic data particle streams converging into unified algorithmic currents (`tech_data_flow.mp4`) with *"COLLECTIVE INTELLIGENCE: 50,000+ trader perspectives unified into real-time consensus"*.
5. **24.5s – 31.0s (The Intelligence Hub)**: Macro institutional financial ticker screen with real-time order flow (`scene_4_financial_screen.mp4`) with *"1 UNIFIED HUB: Sentiment bias, key levels & aggregated signals in one place"*.
6. **31.0s – 37.0s (Structured Confidence)**: Real footage of a relaxed, confident trader executing trades calmly and decisively (`scene_5_confident_trader.mp4`) with *"STRUCTURED CONFIDENCE: From anxiety and hesitation to decisive execution"*.
7. **37.0s – 42.0s (Wall Street Authority)**: Grand architectural establishing shot of the New York Stock Exchange facade (`scene_6_wall_street_nyse.mp4`) with *"WALL STREET EDGE: Institutional-grade perspective in retail hands"*.
8. **42.0s – 48.0s (Brand Resolution & CTA)**: High-converting CrowdWisdomTrading hero brand resolution (`hero_title`) with *"Stop Guessing. Start Knowing. Explore Free at crowdwisdomtrading.com"*.

*Note: All data metrics and overlays are illustrative and educational in full compliance with CrowdWisdomTrading claim guidelines (no guaranteed profit claims, no unregistered advisory claims).*
