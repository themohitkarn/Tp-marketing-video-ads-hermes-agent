import asyncio
import subprocess
import shutil
from pathlib import Path
import edge_tts

AUDIO_DIR = Path(r"D:\OpenMontage\remotion-composer\public\audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
REPO_AUDIO_DIR = Path(r"D:\CWT_Marketing_Video_Ads_Hermes_Agent\assets\audio")
REPO_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "en-US-ChristopherNeural"
RATE = "+3%"


SCRIPT_CWT = [
    {"start": 0.6, "text": "In fast-moving markets, are you catching moves — or caught in noise?"},
    {"start": 6.3, "text": "Fifteen tabs and endless alerts with zero real clarity."},
    {"start": 12.3, "text": "Solo guesswork leaves you entering late and second-guessing every trade."},
    {"start": 18.4, "text": "What if you had the collective wisdom of fifty thousand traders on your side?"},
    {"start": 24.9, "text": "One unified hub for live market sentiment and institutional consensus."},
    {"start": 31.4, "text": "Trade with structured confidence and decisive conviction."},
    {"start": 37.4, "text": "Wall Street intelligence, built for everyday traders."},
    {"start": 42.3, "text": "CrowdWisdomTrading: stop guessing, and start knowing."}
]

SCRIPT_TRADEPULSE = [
    {"start": 0.6, "text": "In fast-moving markets, are you catching moves — or caught in noise?"},
    {"start": 6.3, "text": "Fifteen tabs and endless alerts with zero real clarity."},
    {"start": 12.3, "text": "Solo guesswork leaves you entering late and second-guessing every trade."},
    {"start": 18.4, "text": "What if you had the collective wisdom of fifty thousand traders on your side?"},
    {"start": 24.9, "text": "One unified hub for live market sentiment and institutional consensus."},
    {"start": 31.4, "text": "Trade with structured confidence and decisive conviction."},
    {"start": 37.4, "text": "Wall Street intelligence, built for everyday traders."},
    {"start": 42.3, "text": "TradePulse AI: stop guessing, and start knowing."}
]


async def generate_scene_audio(script, output_filename):
    temp_files = []
    print(f"\nGenerating voiceover segments for {output_filename}...")
    
    for i, item in enumerate(script):
        seg_file = AUDIO_DIR / f"temp_seg_{i}.mp3"
        comm = edge_tts.Communicate(item["text"], VOICE, rate=RATE)
        await comm.save(str(seg_file))
        temp_files.append((item["start"], seg_file))
        print(f"  Scene {i+1} [{item['start']}s]: '{item['text']}'")

    inputs = []
    filter_complex = []
    for i, (start_sec, seg_path) in enumerate(temp_files):
        inputs.extend(["-i", str(seg_path)])
        delay_ms = int(start_sec * 1000)
        filter_complex.append(f"[{i}]adelay={delay_ms}|{delay_ms}[a{i}]")
    
    mix_inputs = "".join([f"[a{i}]" for i in range(len(temp_files))])
    filter_complex.append(f"{mix_inputs}amix=inputs={len(temp_files)}:duration=longest:normalize=0[outa]")
    
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

    for _, seg_path in temp_files:
        if seg_path.exists():
            seg_path.unlink()
            
    shutil.copy2(final_voice, REPO_AUDIO_DIR / output_filename)


async def main():
    await generate_scene_audio(SCRIPT_CWT, "narration_cwt.mp3")
    
    await generate_scene_audio(SCRIPT_TRADEPULSE, "narration_tradepulse.mp3")
    
    shutil.copy2(AUDIO_DIR / "narration_cwt.mp3", AUDIO_DIR / "narration.mp3")
    print("\nAudio generation complete! Set default narration.mp3 -> CrowdWisdomTrading")


if __name__ == "__main__":
    asyncio.run(main())
