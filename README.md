# ShabsTalk - A Voice Assistant

# 🎙️ Voice Assistant using ElevenLabs, Whisper & OpenAI

This is a smart voice assistant that listens to your voice, transcribes it using OpenAI Whisper, processes the query using OpenAI GPT, and speaks out the response using ElevenLabs.

---

## 🔧 Features

- 🎤 Record real-time voice input
- 🧠 Use OpenAI Whisper to transcribe audio
- 🤖 Generate smart responses with OpenAI GPT
- 🗣️ Respond using ElevenLabs realistic speech synthesis
- 📁 Lightweight and runs locally

---

## 🧪 Demo

> “Hey Assistant, what's the weather like today?”  
→ Transcribes → Sends to GPT → Speaks the answer using ElevenLabs

---

## 🛠️ Tech Stack

- Python
- OpenAI Whisper
- ElevenLabs TTS API
- OpenAI GPT API
- Sounddevice & Soundfile
- dotenv

---

## 🚀 Getting Started

To run this project locally, follow these steps:

1. **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/voice-assistant.git
    cd voice-assistant
    ```

2. **(Optional) Create a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install the dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**

   Create a `.env` file in the root directory and add your API keys:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    ELEVENLABS_API_KEY=your_elevenlabs_api_key
    ELEVENLABS_VOICE_ID=your_preferred_voice_id   # optional
    ```

5. **Run the assistant**
    ```bash
    python main.py
    ```

That’s it! Speak into the mic, get a smart reply, and hear it back in a natural voice.

## 🎯 How to Use

1. Run the script:
    ```bash
    python main.py
    ```

2. Speak into your microphone when prompted.

3. The assistant will:
   - Record your voice
   - Transcribe it using Whisper
   - Generate a response via GPT
   - Speak the response aloud using ElevenLabs TTS

4. Repeat the process as needed. Press `Ctrl + C` to stop the program.

---

## 📝 Notes

- Ensure your mic is connected and permissions are granted.
- Whisper works offline if you download the model locally, but using the OpenAI API is faster.
- For best ElevenLabs quality, use a stable internet connection.
- You can change the ElevenLabs voice by modifying the `ELEVENLABS_VOICE_ID` in your `.env`.

---

## 📄 License

This project is licensed under the MIT License.  
Feel free to modify and use it for personal or commercial projects.  
See `LICENSE` file for more details.

---

## 🙏 Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) for powerful speech recognition.
- [ElevenLabs](https://www.elevenlabs.io/) for realistic text-to-speech voices.
- [OpenAI GPT](https://platform.openai.com/) for generating intelligent responses.
- Community packages like `sounddevice`, `soundfile`, and `python-dotenv` for handling audio and environment setup.

---
