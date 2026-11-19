# 🎙️ Whisper Voice AI — Universal Auto-Detect Speech-to-Text

> **A modern, ChatGPT-style voice transcription web app powered by OpenAI Whisper and intelligent multi-language auto-detection.**
> 
> Automatically detects and transcribes speech in **Gujarati, Hindi, English, Marathi, Bengali, Spanish, French, German, Arabic, Russian, Japanese, and 99+ languages** directly into their native scripts with **zero configuration required**.

---

## 🌟 Key Features

- **🌐 Zero-Config Universal Auto-Detection**: Speak in English, Gujarati, Hindi, Marathi, Spanish, Arabic, or any language — no dropdowns, no settings needed. The system auto-detects the spoken language and types out the text in the correct native script.
- **💬 ChatGPT-Style Web Interface**: Clean, dark-mode, distraction-free conversational UI built with Flask and vanilla modern JavaScript.
- **⚡ Blazing Fast Speed (~1s)**: Optimized with concurrent multi-engine speech recognition and FFmpeg audio preprocessing to deliver results in ~1 second.
- **🎙️ Dual Usage Modes**:
  1. **Web UI**: Open in any browser, click the mic, speak, and watch words type directly into the chat input.
  2. **Terminal Mode**: Run `speak.bat` or `python live_speak.py` to record and transcribe directly in your command line.
- **📁 File Upload Support**: Attach existing audio files (`.wav`, `.mp3`, `.m4a`, `.ogg`, `.webm`) to transcribe them instantly.

---

## 🚀 Quick Start for Team Members (One-Click Setup)

### 1. Clone the Repository
```bash
git clone https://github.com/sahilpvnerds-hub/whisper-any-language-voice-to-text.git
cd whisper-any-language-voice-to-text
```

### 2. Run Setup (Windows)
Double-click **`setup.bat`** (or run in Command Prompt):
```cmd
setup.bat
```
*This will check for Python, ensure FFmpeg is installed, and install all required Python packages.*

### 3. Launch the Web UI
Double-click **`run_web_ui.bat`**:
```cmd
run_web_ui.bat
```
Your default browser will automatically open:
👉 **http://127.0.0.1:5000**

---

## 🛠️ Manual Installation Guide

### Prerequisites
- **Python 3.9+** (Tested on Python 3.10 - 3.14)
- **FFmpeg** (Required for audio decoding)

#### Step 1: Install FFmpeg
- **Windows (PowerShell)**:
  ```powershell
  winget install Gyan.FFmpeg
  ```
- **macOS (Homebrew)**:
  ```bash
  brew install ffmpeg
  ```
- **Ubuntu / Debian**:
  ```bash
  sudo apt update && sudo apt install ffmpeg
  ```

#### Step 2: Install Python Packages
```bash
pip install -r requirements.txt
```

#### Step 3: Run the Application
```bash
python app.py
```
Open **`http://127.0.0.1:5000`** in your browser.

---

## 🧪 Tested & Verified Languages

The engine has been thoroughly tested and verified with audio samples across all major language families:

| Language | Native Script Example Output |
|---|---|
| **English** | `hello everyone my name is Sahil Patil and I am testing voice recognition in English` |
| **Gujarati (ગુજરાતી)** | `મારું નામ સાહિલ છે ને હું ગુજરાતી આવું છું` |
| **Hindi (हिन्दी)** | `मेरा नाम साहिल है और मैं गुजरात से आता हूं` |
| **Marathi (मराठी)** | `माझे नाव साहिल आहे आणि मी भारतात राहतो` |
| **Bengali (বাংলা)** | `আমার নাম সাহিল এন্ড আমি ভারতে থাকি` |
| **Spanish (Español)** | `hola a todos mi nombre es sagil y hablo español` |
| **French (Français)** | `bonjour tout le monde je m'appelle Saïd` |
| **German (Deutsch)** | `guten Tag mein Name ist Sahel` |
| **Arabic (العربية)** | `مرحبا بالجميع اسمي ساحل واتحدث العربيه` |
| **Russian (Русский)** | `Всем привет Меня зовут сахил` |
| **Japanese (日本語)** | `皆さんこんにちは私の名前はさひるです` |

---

## 📁 Project Structure

```
whisper-any-language-voice-to-text/
│
├── app.py                  # Core Flask server & Universal Auto-Detect engine
├── setup.bat               # One-click dependency & FFmpeg setup for Windows
├── run_web_ui.bat          # One-click launcher for the ChatGPT-style Web UI
├── live_speak.py           # Terminal-based microphone speech-to-text script
├── speak.bat               # One-click launcher for terminal voice recording
├── requirements.txt        # Python package dependencies
├── .gitignore              # Ignores large binaries & temp files
│
├── templates/
│   └── index.html          # Clean, ChatGPT-style responsive Web UI
│
├── whisper/                # OpenAI Whisper core source code & model logic
└── README.md               # Project documentation
```

---

## 👤 Author & Credits

- Developed & Customized by **Sahil Patel** ([@sahilpvnerds-hub](https://github.com/sahilpvnerds-hub))
- Core Transformer Speech Recognition powered by **OpenAI Whisper**
- Audio decoding and conversion powered by **FFmpeg**

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
