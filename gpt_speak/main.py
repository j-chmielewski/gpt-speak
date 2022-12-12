from playsound import playsound
from pydub import AudioSegment
from typing import Dict
from revChatGPT.revChatGPT import Chatbot
import sounddevice
import click
import whisper
from gtts import gTTS

from gpt_speak.recording import listen


REC_FILE = "/tmp/gptrec.wav"
SPK_FILE = "/tmp/gptspk.wav"
SAMPLE_RATE = 44100
REC_DURATION = 10

model = whisper.load_model("small")


def transcribe() -> str:
    print("Transcribing")
    result = model.transcribe(REC_FILE)
    transcription = str(result.get("text", ""))
    print("Transcription:", transcription)
    return transcription


def get_response(chatbot: Chatbot, msg: str) -> Dict:
    print("Querying AI overlords")
    response = chatbot.get_chat_response(msg, output="text")
    print("They have spoken:", response["message"])
    return response


def speak(msg: str, lang: str) -> None:
    print("Speaking")
    spk = gTTS(text=msg, lang=lang, slow=False)
    spk.save(SPK_FILE)
    # Speed up & play audio
    audio = AudioSegment.from_file(SPK_FILE)
    faster_audio = audio.speedup(playback_speed=1.5)
    faster_audio.export(SPK_FILE, format="wav")
    playsound(f"{SPK_FILE}")


def init_bot(token) -> Chatbot:
    config = {
        "session_token": token,
    }
    return Chatbot(config, conversation_id=None)


@click.command()
@click.option("--token", help="Token from gpt chat cookie", required=True)
@click.option("--lang", help="Language to use for speech synthesis", default="en")
def main(token: str, lang: str):
    bot = init_bot(token)
    for _ in listen():
        msg = transcribe()
        response = get_response(bot, msg)
        speak(response["message"], lang)


if __name__ == "__main__":
    main()
