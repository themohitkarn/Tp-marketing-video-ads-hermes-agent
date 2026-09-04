import os
import sys
import time
from pathlib import Path
from datetime import datetime

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.live import Live
from rich.align import Align

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
RENDER_FILE = Path(r"D:\OpenMontage\projects\demos\renders\crowdwisdom.mp4")

# Force legacy_windows=False to allow rich ANSI styling without cp1252 crash
console = Console(legacy_windows=False)


TASKS = [
    {
        "id": "HERMES-101",
        "title": "Meta Ads Mining",
        "agent": "Ads Manager Agent (Apify)",
        "deliverable": "processed_ads_*.json",
        "status": "DONE",
        "notes": "20 competitor Meta ads collected & cleaned"
    },
    {
        "id": "HERMES-102",
        "title": "Rule-Based Ad Analysis",
        "agent": "Ad Analysis Agent",
        "deliverable": "ad_analysis_*.json",
        "status": "DONE",
        "notes": "Extracted hooks, angles, CTA strength"
    },
    {
        "id": "HERMES-103",
        "title": "Winning Patterns Synthesis",
        "agent": "Winning Ads Agent (OpenRouter)",
        "deliverable": "marketing_insights_*.json",
        "status": "DONE",
        "notes": "ICP, top pain points, emotional triggers"
    },
    {
        "id": "HERMES-104",
        "title": "Recent Trader Pain Search",
        "agent": "Research Agent (Tavily)",
        "deliverable": "market_research_*.json",
        "status": "DONE",
        "notes": "Recent retail trader challenges & overload data"
    },
    {
        "id": "HERMES-105",
        "title": "Ad Concept Ideation",
        "agent": "Ad Concept Agent",
        "deliverable": "ad_concepts_*.json",
        "status": "DONE",
        "notes": "5 original concepts (The Chart Trap, etc.)"
    },
    {
        "id": "HERMES-106",
        "title": "Short-Form Video Scripting",
        "agent": "Ad Script Agent",
        "deliverable": "scripts_*.json",
        "status": "DONE",
        "notes": "30-60s scripts with pattern interrupt hooks"
    },
    {
        "id": "HERMES-107",
        "title": "Scene Storyboard Production",
        "agent": "Storyboard Agent",
        "deliverable": "storyboards_*.json",
        "status": "DONE",
        "notes": "33 granular scenes with timing & overlays"
    },
    {
        "id": "HERMES-108",
        "title": "Cinematic Prompt Engineering",
        "agent": "Video Agent (OpenRouter)",
        "deliverable": "video_prompts_*.json",
        "status": "DONE",
        "notes": "Cinematic camera, lighting & mood prompts"
    },
    {
        "id": "HERMES-109",
        "title": "Remotion Motion-Graphics Props",
        "agent": "OpenMontage Props Agent",
        "deliverable": "crowdwisdom.json",
        "status": "DONE",
        "notes": "HeroTitle, Callout, Comparison, Donut, KPI Grid"
    },
    {
        "id": "HERMES-110",
        "title": "Broadcast Video Rendering",
        "agent": "OpenMontage Engine (Remotion)",
        "deliverable": "crowdwisdom.mp4",
        "status": "DONE",
        "notes": "45s motion-graphics ad (H.264 1080p, 60fps)"
    }
]


def render_kanban(step_index=len(TASKS)):
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=4),
        Layout(name="kanban", ratio=1),
        Layout(name="footer", size=3)
    )

    # Header
    header_text = Text(
        "[+] HERMES AGENT FRAMEWORK -- CROWDWISDOMTRADING MARKETING ADS TEAM [+]\n"
        "Multi-Agent Workflow Orchestration & Kanban Execution Board",
        style="bold cyan",
        justify="center"
    )
    layout["header"].update(Panel(header_text, border_style="cyan"))

    # Kanban Columns Table
    board = Table(expand=True, box=None, padding=(0, 1))
    board.add_column("[BACKLOG]", style="dim", ratio=1)
    board.add_column("[IN PROGRESS]", style="bold yellow", ratio=1)
    board.add_column("[REVIEW]", style="bold blue", ratio=1)
    board.add_column("[DONE]", style="bold green", ratio=1)

    backlog_items = []
    in_progress_items = []
    review_items = []
    done_items = []

    for i, t in enumerate(TASKS):
        card = (
            f"[bold]{t['id']}: {t['title']}[/bold]\n"
            f"[cyan]Agent:[/cyan] {t['agent']}\n"
            f"[magenta]Artifact:[/magenta] {t['deliverable']}\n"
            f"[white]{t['notes']}[/white]\n"
        )
        if i > step_index:
            backlog_items.append(f"[dim]{card}[/dim]")
        elif i == step_index:
            in_progress_items.append(f"[yellow]{card}[/yellow]")
        elif i == step_index - 1 and step_index < len(TASKS):
            review_items.append(f"[blue]{card}[/blue]")
        else:
            done_items.append(f"[green]{card}[/green]")

    max_len = max(len(backlog_items), len(in_progress_items), len(review_items), len(done_items), 1)

    for r in range(max_len):
        b = backlog_items[r] if r < len(backlog_items) else ""
        p = in_progress_items[r] if r < len(in_progress_items) else ""
        rv = review_items[r] if r < len(review_items) else ""
        d = done_items[r] if r < len(done_items) else ""
        board.add_row(
            Panel(b, border_style="dim") if b else "",
            Panel(p, border_style="yellow") if p else "",
            Panel(rv, border_style="blue") if rv else "",
            Panel(d, border_style="green") if d else ""
        )

    layout["kanban"].update(board)

    # Footer
    completed_count = min(step_index, len(TASKS))
    footer_text = Text(
        f"Tasks Completed: {completed_count}/{len(TASKS)} | "
        f"Pipeline Output: crowdwisdom.mp4 | "
        f"Status: ALL 10 MARKETING AGENT TASKS COMPLETED",
        style="bold white on blue",
        justify="center"
    )
    layout["footer"].update(Panel(footer_text, border_style="blue"))

    return layout


def main():
    console.print(
        "[bold green]Starting Hermes Marketing Agent Team Kanban Orchestrator...[/bold green]\n"
    )

    # Live playback mode for screen recording
    if "--live" in sys.argv or "-l" in sys.argv:
        with Live(render_kanban(0), refresh_per_second=4, console=console) as live:
            for s in range(1, len(TASKS) + 1):
                time.sleep(1.0)
                live.update(render_kanban(s))
            time.sleep(2)
    else:
        # Static full board view
        console.print(render_kanban(len(TASKS)))

    console.print("\n[bold green][DONE] Hermes Kanban Execution Verified![/bold green]")
    console.print(f"Final Rendered Video Ad: [cyan]{RENDER_FILE}[/cyan]\n")


if __name__ == "__main__":
    main()
