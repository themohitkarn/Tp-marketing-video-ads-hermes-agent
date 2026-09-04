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

## 🎬 Creative Video Ad Structure (47 Seconds)

Adhering strictly to the requirement **"Dont make text ads. this is not the assessment"**, the video combines:
1. **0.0s – 5.0s**: Animated volatile market price action (`line_chart`) with dynamic draw animation.
2. **5.0s – 10.0s**: Notification chaos & 15+ tabs overload warning box (`callout`).
3. **10.0s – 16.5s**: Direct side-by-side contrast: Fragmented Noise vs. CrowdWisdom Hub (`comparison`).
4. **16.5s – 22.5s**: Multi-source data convergence card (`stat_card`).
5. **22.5s – 29.0s**: Real-time collective sentiment consensus breakdown (`pie_chart` donut).
6. **29.0s – 35.5s**: Live dashboard transformation with cascade animation (`kpi_grid`).
7. **35.5s – 40.5s**: Noise filtration progress bar (`progress_bar`).
8. **40.5s – 47.0s**: High-converting closing hook and CTA (`hero_title`).

*Note: All data metrics are explicitly framed as illustrative/sample platform visualizations in full compliance with CrowdWisdomTrading claim policies.*
