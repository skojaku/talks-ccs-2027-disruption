"""Narrated movie with Kokoro TTS (kokoro-onnx). Run with an interpreter that has kokoro-onnx and soundfile:
    python make_movie_kokoro.py MODEL.onnx VOICES.bin [voice] [speed]"""
import subprocess, sys, json
from pathlib import Path
import soundfile as sf
from kokoro_onnx import Kokoro
from script import N

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "narration" / "build_kokoro"
OUT.mkdir(exist_ok=True)
MODEL, VOICES = sys.argv[1], sys.argv[2]
VOICE = sys.argv[3] if len(sys.argv) > 3 else "af_heart"
SPEED = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
LONG = {1, 7, 19, 20, 28, 32, 40, 41, 60, 66, 72, 73, 83, 86, 87, 93}
sh = lambda *a: subprocess.run(a, check=True, capture_output=True)
dur = lambda f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                     capture_output=True, text=True).stdout)
k = Kokoro(MODEL, VOICES)
segs, total = [], 0.0
for i in range(1, 95):
    wav = OUT / f"a{i:03d}.wav"
    samples, sr = k.create(N[i], voice=VOICE, speed=SPEED, lang="en-us")
    sf.write(str(OUT / f"raw{i:03d}.wav"), samples, sr)
    pause = 1.1 if i in LONG else 0.5
    sh("ffmpeg", "-y", "-i", str(OUT / f"raw{i:03d}.wav"), "-af", f"apad=pad_dur={pause}", "-ar", "44100", "-ac", "1", str(wav))
    d = dur(wav); total += d
    seg = OUT / f"seg{i:03d}.mp4"
    sh("ffmpeg", "-y", "-loop", "1", "-framerate", "10", "-i", str(ROOT / f"review/slide.{i:03d}.png"), "-i", str(wav),
       "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:white,format=yuv420p",
       "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage", "-c:a", "aac", "-b:a", "128k", "-t", f"{d:.3f}", str(seg))
    segs.append((i, d))
(OUT / "list.txt").write_text("".join(f"file 'seg{i:03d}.mp4'\n" for i, _ in segs))
sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(OUT / "list.txt"), "-c", "copy", str(ROOT / "ccs-2027-narrated-kokoro.mp4"))
json.dump(segs, open(OUT / "timing.json", "w"))
print(f"total {total:.1f} s = {total/60:.2f} min")
