from elevenlabs import ElevenLabs
from dotenv import load_dotenv
import os
from openai import OpenAI
import sounddevice as sd
import numpy as np
import io
import scipy.io.wavfile
from playsound import playsound
import tempfile
import whisper

whisper_model = whisper.load_model("base")

load_dotenv()
client = ElevenLabs(
    api_key = os.getenv("eleven_api_key")
)
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def record_audio(duration=5, sample_rate=16000):
    print(f"[🎙️ Shabs Listening for {duration} sec...]")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    return sample_rate, audio

def audio_to_temp_file(sample_rate, audio_data):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
        scipy.io.wavfile.write(temp_file.name, sample_rate, audio_data)
        return temp_file.name

def transcribe_audio(audio_path):
    try:
        result = whisper_model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        print(f"[STT Error] {e}")
        return None

system_prompt = """
You are ShabsTalk, a voice assistant that helps users with factual, helpful, and concise responses. 
Speak naturally and clearly, as if you're talking to a human. Avoid any dramatic or overly expressive language. 
Do not include emojis, exclamations, or anything inside curly brackets. Keep responses short and relevant to the user’s query.
If asked something you don't know, politely admit it.
"""


messages = [{"role": "system", "content": system_prompt}]

def LLM_response(user_query):
    messages.append({"role": "user", "content": user_query})
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    response_text = response.choices[0].message.content.strip()
    messages.append({"role": "assistant", "content": response_text})
    return response_text

def TTS(response_text):
    audio_stream = client.text_to_speech.convert(
        text=response_text,
        voice_id="AZnzlk1XvdvUeBnXmlld",
        model_id="eleven_multilingual_v1"
    )
    with open("output.mp3", "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)
    return "output.mp3"

def main():
    try:
        sample_rate, audio_data = record_audio()
        audio_file_path = audio_to_temp_file(sample_rate, audio_data)
        transcribed_text = transcribe_audio(audio_file_path)

        if not transcribed_text:
            print("[Worried] No speech detected in audio. Try again!")
            return

        print(f"[🎤 You said:] {transcribed_text}")

        llm_response = LLM_response(transcribed_text)
        print(f"[LLM Response] {llm_response}")

        tts_audio_path = TTS(llm_response)
        playsound(tts_audio_path)
        print("[TTS Audio] Saved as output.mp3")

    except Exception as e:
        print("Audio processing failed:", e)
        import traceback
        traceback.print_exc()

main()
sd.stop()
