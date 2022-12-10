import os
from typing import Dict
from revChatGPT.revChatGPT import Chatbot
import click
import whisper
import sounddevice as sd
import soundfile as sf
from gtts import gTTS


REC_FILE = "/tmp/gptrec.wav"
SPK_FILE = "/tmp/gptspk.wav"
LANG = "en"
PLAYER = "mpg123 -q"
SAMPLE_RATE = 44100
REC_DURATION = 10

model = whisper.load_model("small")


def listen() -> None:
    print("Recording")
    myrecording = sd.rec(int(REC_DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=2)
    sd.wait()
    sf.write(REC_FILE, myrecording, SAMPLE_RATE)


def transcribe() -> str:
    print("Transcribing")
    result = model.transcribe(REC_FILE)
    return str(result.get("text", ""))


def get_response(chatbot: Chatbot, msg: str) -> Dict:
    return chatbot.get_chat_response(msg, output="text")


def speak(msg: str) -> None:
    print("Speaking")
    spk = gTTS(text=msg, lang=LANG, slow=False)
    spk.save(SPK_FILE)
    os.system(f"{PLAYER} {SPK_FILE}")


def init_bot(token) -> Chatbot:
    config = {
        "session_token": token,
    }
    return Chatbot(config, conversation_id=None)


@click.command()
@click.option("--token", help="Session token from gpt chat cookie", required=True)
def main(token: str):
    bot = init_bot(token)
    listen()
    msg = transcribe()
    response = get_response(bot, msg)
    speak(response["message"])


if __name__ == "__main__":
    main()
