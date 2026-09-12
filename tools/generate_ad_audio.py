import asyncio
import subprocess
import shutil
from pathlib import Path
import edge_tts

AUDIO_DIR = Path(r"D:\OpenMontage\remotion-composer\public\audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
REPO_AUDIO_DIR = Path(r"D:\CWT_Marketing_Video_Ads_Hermes_Agent\assets\audio")
REPO_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Voice configuration: authoritative, broadcast commercial style
VOICE = "en-US-ChristopherNeural"

# Scene scripts timed to video cuts (48 seconds total)
SCRIPT_CWT = [
    {"start": 0.5, "text": "Volatile markets move fast. Are you catching the moves, or getting caught in the noise?"},
    {"start": 6.3, "text": "Fifteen open tabs. Fifty Telegram channels. Endless alerts, but zero high conviction clarity."},
    {"start": 12.3, "text": "Solo guesswork leaves you entering late and second guessing every trade."},
    {"start": 18.5, "text": "What if you had the collective intelligence of over fifty thousand traders working for you?"},
    {"start": 24.8, "text": "One unified hub. Real-time sentiment bias, key support levels, and institutional perspective."},
    {"start": 31.3, "text": "Trade with structured confidence. Stop the anxiety, and start executing with conviction."},
    {"start": 37.3, "text": "The power of Wall Street consensus, right in your hands."},
    {"start": 42.5, "text": "CrowdWisdomTrading. Stop guessing. Start knowing. Explore free today."}
]

SCRIPT_TRADEPULSE = [
    {"start": 0.5, "text": "Volatile markets move fast. Are you catching the moves, or getting caught in the noise?"},
    {"start": 6.3, "text": "Fifteen open tabs. Fifty Telegram channels. Endless alerts, but zero high conviction clarity."},
    {"start": 12.3, "text": "Solo guesswork leaves you entering late and second guessing every trade."},
    {"start": 18.5, "text": "What if you had the collective intelligence of over fifty thousand traders working for you?"},
    {"start": 24.8, "text": "One unified hub. Real-time sentiment bias, key support levels, and institutional perspective."},
    {"start": 31.3, "text": "Trade with structured confidence. Stop the anxiety, and start executing with conviction."},
    {"start": 37.3, "text": "The power of Wall Street consensus, right in your hands."},
    {"start": 42.5, "text": "TradePulse AI. Stop guessing. Start knowing. Explore free today at tradepulse.ai."}
]


async def generate_scene_audio(script, output_filename):
    temp_files = []
    print(f"\nGenerating voiceover segments for {output_filename}...")
    
    for i, item in enumerate(script):
        seg_file = AUDIO_DIR / f"temp_seg_{i}.mp3"
        comm = edge_tts.Communicate(item["text"], VOICE, rate="+3%")
        await comm.save(str(seg_file))
        temp_files.append((item["start"], seg_file))
        print(f"  Generated scene {i+1}: '{item['text'][:45]}...'")

    # Combine into 48s timed master track using ffmpeg adelay and amix
    inputs = []
    filter_complex = []
    for i, (start_sec, seg_path) in enumerate(temp_files):
        inputs.extend(["-i", str(seg_path)])
        delay_ms = int(start_sec * 1000)
        filter_complex.append(f"[{i}]adelay={delay_ms}|{delay_ms}[a{i}]")
    
    mix_inputs = "".join([f"[a{i}]" for i in range(len(temp_files))])
    # Boost voice track so it cuts through clearly over background music
    filter_complex.append(f"{mix_inputs}amix=inputs={len(temp_files)}:duration=longest:dropout_transition=2,volume={len(temp_files)}*1.2[outa]")
    
    final_voice = AUDIO_DIR / output_filename
    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", ";".join(filter_complex),
        "-map", "[outa]",
        "-t", "48",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        str(final_voice)
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    print(f"Master voiceover created: {final_voice}")

    # Clean up temp segments
    for _, seg_path in temp_files:
        if seg_path.exists():
            seg_path.unlink()
            
    # Copy to repo assets
    shutil.copy2(final_voice, REPO_AUDIO_DIR / output_filename)


async def main():
    # 1. Generate CrowdWisdomTrading voiceover (for Gilad)
    await generate_scene_audio(SCRIPT_CWT, "narration_cwt.mp3")
    
    # 2. Generate TradePulse AI voiceover (for LinkedIn)
    await generate_scene_audio(SCRIPT_TRADEPULSE, "narration_tradepulse.mp3")
    
    # Set default narration.mp3 to CWT for Gilad review
    shutil.copy2(AUDIO_DIR / "narration_cwt.mp3", AUDIO_DIR / "narration.mp3")
    shutil.copy2(AUDIO_DIR / "narration_cwt.mp3", REPO_AUDIO_DIR / "narration.mp3")
    print("\nAudio generation complete! Set default narration.mp3 -> CrowdWisdomTrading")

    # Also save a copy of this script into tools/generate_ad_audio.py
    src_code = Path(__file__).read_text(encoding="utf-8")
    (Path(r"D:\CWT_Marketing_Video_Ads_Hermes_Agent\tools\generate_ad_audio.py")).write_text(src_code, encoding="utf-8")
    print("Saved to tools/generate_ad_audio.py")


if __name__ == "__main__":
    asyncio.run(main())
