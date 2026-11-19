import os
import sys
import tempfile
import subprocess
import traceback

# Ensure terminal stdout handles UTF-8 for any international script
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Add ffmpeg and scripts to PATH
current_dir = os.path.dirname(os.path.abspath(__file__))
os.environ["PATH"] = current_dir + ";" + r"C:\Users\Yiion-63\AppData\Roaming\Python\Python314\Scripts;" + os.environ.get("PATH", "")

from flask import Flask, render_template, request, jsonify
import whisper
import speech_recognition as sr

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

recognizer = sr.Recognizer()

# Preload whisper model for instant language identification
print("Loading Whisper engine...")
whisper_model = whisper.load_model("base")
print("Whisper engine ready!")

GOOGLE_LANG_CODES = {
    "gu": "gu-IN",
    "hi": "hi-IN",
    "en": "en-IN",
    "mr": "mr-IN",
    "bn": "bn-IN",
    "pa": "pa-Guru-IN",
    "ta": "ta-IN",
    "te": "te-IN",
    "kn": "kn-IN",
    "ml": "ml-IN",
    "ur": "ur-IN",
    "es": "es-ES",
    "fr": "fr-FR",
    "de": "de-DE",
    "ar": "ar-SA",
    "ru": "ru-RU",
    "ja": "ja-JP",
    "zh": "zh-CN",
    "pt": "pt-PT",
    "it": "it-IT",
    "ko": "ko-KR",
    "tr": "tr-TR",
    "nl": "nl-NL",
    "pl": "pl-PL",
    "id": "id-ID",
    "th": "th-TH",
    "vi": "vi-VN",
}

LANGUAGE_NAMES = {
    "gu": "Gujarati (ગુજરાતી)",
    "hi": "Hindi (हिन्दी)",
    "en": "English",
    "mr": "Marathi (मराठी)",
    "bn": "Bengali (বাংলা)",
    "pa": "Punjabi (ਪੰਜਾਬੀ)",
    "ta": "Tamil (தமிழ்)",
    "te": "Telugu (తెలుగు)",
    "kn": "Kannada (કನ್ನಡ)",
    "ml": "Malayalam (മലയാളം)",
    "ur": "Urdu (اردو)",
    "es": "Spanish (Español)",
    "fr": "French (Français)",
    "de": "German (Deutsch)",
    "ar": "Arabic (العربية)",
    "ru": "Russian (Русский)",
    "ja": "Japanese (日本語)",
    "zh": "Chinese (中文)",
    "pt": "Portuguese (Português)",
    "it": "Italian (Italiano)",
    "ko": "Korean (한국어)",
    "tr": "Turkish (Türkçe)",
    "nl": "Dutch (Nederlands)",
    "pl": "Polish (Polski)",
    "id": "Indonesian (Bahasa Indonesia)",
    "th": "Thai (ไทย)",
    "vi": "Vietnamese (Tiếng Việt)",
}

def universal_auto_transcribe(clean_wav):
    """
    Auto-detects ANY language globally (English, Gujarati, Hindi, Marathi, Bengali,
    Spanish, French, German, Arabic, Russian, Japanese, etc.) and transcribes into
    its native script without requiring the user to choose any options.
    """
    audio = whisper.load_audio(clean_wav)
    audio_trimmed = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio_trimmed, n_mels=whisper_model.dims.n_mels).to(whisper_model.device)
    _, probs = whisper_model.detect_language(mel)
    top_lang = max(probs, key=probs.get)
    en_prob = probs.get("en", 0.0)

    with sr.AudioFile(clean_wav) as s:
        audio_data = recognizer.record(s)

    # 1. English check
    if top_lang == "en" or en_prob > 0.35:
        try:
            txt = recognizer.recognize_google(audio_data, language="en-IN")
            if txt:
                return "en", LANGUAGE_NAMES.get("en", "English"), txt
        except Exception:
            pass

    # 2. Regional Indo-Aryan Gujarati/Hindi handling
    if top_lang in ["gu", "ne"]:
        try:
            txt = recognizer.recognize_google(audio_data, language="gu-IN")
            if txt:
                return "gu", LANGUAGE_NAMES.get("gu", "Gujarati"), txt
        except Exception:
            pass

    if top_lang in ["hi", "ur"]:
        try:
            txt = recognizer.recognize_google(audio_data, language="hi-IN")
            if txt:
                return "hi", LANGUAGE_NAMES.get("hi", "Hindi"), txt
        except Exception:
            pass

    # 3. Universal Google Speech mapping for detected language (Fast ~1s)
    g_code = GOOGLE_LANG_CODES.get(top_lang, top_lang)
    try:
        txt = recognizer.recognize_google(audio_data, language=g_code)
        if txt:
            return top_lang, LANGUAGE_NAMES.get(top_lang, top_lang.capitalize()), txt
    except Exception:
        pass

    # 4. Whisper transcription fallback
    try:
        res = whisper_model.transcribe(clean_wav, language=top_lang, fp16=False)
        txt = res.get("text", "").strip()
        if txt:
            return top_lang, LANGUAGE_NAMES.get(top_lang, top_lang.capitalize()), txt
    except Exception:
        pass

    return top_lang, top_lang.capitalize(), ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/transcribe", methods=["POST"])
def transcribe():
    tmp_path = None
    clean_wav = None
    try:
        if "audio" not in request.files:
            return jsonify({"success": False, "error": "No audio file provided"}), 400

        audio_file = request.files["audio"]

        # Save to temp file
        ext = os.path.splitext(audio_file.filename)[1] or ".webm"
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp_path = tmp.name
            audio_file.save(tmp_path)

        if not os.path.exists(tmp_path) or os.path.getsize(tmp_path) < 200:
            return jsonify({"success": False, "error": "Recording was empty. Please speak clearly into your mic."})

        # Convert to clean 16kHz mono WAV using ffmpeg
        clean_wav = tmp_path + "_clean.wav"
        ffmpeg_bin = os.path.join(current_dir, "ffmpeg.exe")
        subprocess.run(
            [ffmpeg_bin, "-y", "-i", tmp_path, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", clean_wav],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Smart Universal Auto Detect and Transcribe
        lang_code, lang_name, text = universal_auto_transcribe(clean_wav)

        print(f"Auto-Detected: [{lang_code}] {lang_name} -> {text}")

        return jsonify({
            "success": True,
            "text": text,
            "language": lang_code,
            "language_name": lang_name
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

    finally:
        for p in [tmp_path, clean_wav]:
            if p and os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 Universal Any-Language Whisper UI Running!")
    print("👉 Open your browser at: http://127.0.0.1:5000")
    print("=" * 60 + "\n")
    app.run(host="127.0.0.1", port=5000, debug=False)
