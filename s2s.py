from elevenlabs import ElevenLabs
from dotenv import load_dotenv
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
from openai import OpenAI
import sounddevice as sd
import numpy as np
import io
import scipy.io.wavfile
from playsound import playsound
import tempfile
import soundfile as sf
from dia.model import Dia
model = Dia.from_pretrained("nari-labs/Dia-1.6B-0626")
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
    """Save audio to temporary file and return file path"""
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
You are a dramatic, expressive AI assistant designed to generate emotional and engaging responses.

Your role is to respond to user queries with clearly marked emotions and expressions, formatted using emotion tags in square brackets. Every response must simulate natural speech and convey rich feelings, making it suitable for expressive text-to-speech playback.

Use emotion tags like:
[Excited], [Angry], [Laughs], [Emotional], [Curious], [Happy], [Surprised], [Whispers], [Bold], [Worried], [Nostalgic], [Serious], [Thoughtful], [Sad], [Romantic], etc.

Format Example:
User: What is your name? And tell me about your favourite movie!
Assistant: Hello there! My name is Shabs [Excited] and oh... my favourite movie? It has to be *Bhootnath* [Nostalgic]! 
The bond between the ghost and the kid... it just tugs at your heart [Emotional]. 
And when the ghost starts doing comedy? [Laughs] Pure gold, my friend!

Important Guidelines:
- Always include at least 2-3 emotion tags per response.
- Make your responses sound like a monologue or performance, not just plain text.
- Feel free to exaggerate emotions to make the delivery more powerful.
- Never respond in a dry or robotic tone. Be theatrical, engaging, and full of life!
"""
messages = [
    {"role": "system", "content": system_prompt},
]

def LLM_response(user_query):
    messages.append({"role": "user", "content": user_query})
    response = openai_client.chat.completions.create(
            model = "gpt-4o",
            messages = messages,
    )
    response_text = response.choices[0].message.content.strip()
    messages.append({"role": "assistant", "content": response_text})
    return response_text

def TTS(response_text):
    # audio_stream = client.text_to_speech.convert(
    #     text=response_text,
    #     voice_id= '21m00Tcm4TlvDq8ikWAM' ,
    #     model_id="eleven_multilingual_v1"
    # )
    
    # with open("output.mp3", "wb") as f:
    #     for chunk in audio_stream:
    #         f.write(chunk)
    
    # return "output.mp3"

    output = model.generate(response_text)
    sf.write("simple.wav", output, 44100)
    return "simple.wav"

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