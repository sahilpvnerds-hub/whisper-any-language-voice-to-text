import os
import sys

# Ensure local directory with ffmpeg.exe and scripts is in PATH
os.environ["PATH"] = r"D:\whisper;C:\Users\Yiion-63\AppData\Roaming\Python\Python314\Scripts;" + os.environ.get("PATH", "")

import whisper

def main():
    print("Loading Whisper model (tiny)...")
    model = whisper.load_model("tiny")

    audio_file = "sample.wav"
    print(f"Transcribing '{audio_file}'...")
    result = model.transcribe(audio_file)

    print("\n--- Detected Language ---")
    print(result.get("language", "Unknown"))

    print("\n--- Transcription Text ---")
    print(result["text"])

    print("\n--- Detailed Segments ---")
    for segment in result["segments"]:
        print(f"[{segment['start']:.2f}s -> {segment['end']:.2f}s] {segment['text']}")

if __name__ == "__main__":
    main()
