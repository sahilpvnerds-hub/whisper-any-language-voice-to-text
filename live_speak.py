import sys
import os
import time
import threading
import numpy as np

# Ensure terminal prints UTF-8 (Hindi, Gujarati, Tamil, etc.)
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Ensure ffmpeg and scripts are in PATH
os.environ["PATH"] = r"D:\whisper;C:\Users\Yiion-63\AppData\Roaming\Python\Python314\Scripts;" + os.environ.get("PATH", "")

import sounddevice as sd
from scipy.io.wavfile import write
import whisper

SAMPLE_RATE = 16000
CHANNELS = 1
TEMP_WAV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_voice.wav")

def record_audio():
    audio_frames = []
    stop_event = threading.Event()

    def callback(indata, frames, time_info, status):
        if not stop_event.is_set():
            audio_frames.append(indata.copy())

    # Start audio input stream
    stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype="int16", callback=callback)
    with stream:
        print("\n🔴 Recording... Speak into your microphone now!")
        input("👉 Press [ENTER] when you are DONE speaking...\n")
        stop_event.set()

    if not audio_frames:
        return None

    audio_data = np.concatenate(audio_frames, axis=0)
    write(TEMP_WAV, SAMPLE_RATE, audio_data)
    return TEMP_WAV

def main():
    print("=" * 65)
    print("      🎙️ OPENAI WHISPER - LIVE VOICE-TO-TEXT RECORDER")
    print("=" * 65)
    print("Loading Whisper model (base)... Please wait a few seconds...")
    # 'base' model is fast and supports 99+ languages automatically
    model = whisper.load_model("base")
    print("✅ Model loaded! Ready to listen.\n")

    while True:
        print("-" * 65)
        choice = input("👉 Press [ENTER] to start speaking (or type 'q' and press ENTER to quit): ").strip().lower()
        if choice == "q":
            print("\nExiting. Goodbye!")
            break

        wav_file = record_audio()
        if wav_file is None or os.path.getsize(wav_file) < 1000:
            print("⚠️ No audio detected. Please try again.")
            continue

        print("⏳ Transcribing with Whisper... (Detecting language)")
        try:
            result = model.transcribe(wav_file, fp16=False)
            detected_lang = result.get("language", "Unknown")
            transcription = result.get("text", "").strip()

            print("\n" + "=" * 65)
            print(f"🌐 Detected Language : {detected_lang.upper()}")
            print(f"📝 You Said          : {transcription}")
            print("=" * 65 + "\n")
        except Exception as e:
            print(f"❌ Error transcribing audio: {e}\n")

if __name__ == "__main__":
    main()
