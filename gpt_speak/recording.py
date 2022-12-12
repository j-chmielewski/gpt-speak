from typing import Generator
from datetime import datetime, timedelta
import pyaudio
import wave
import numpy as np

# Set the recording parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
REC_FILE = "/tmp/gptrec.wav"
# Set the threshold for the audio amplitude (between 0 and 1)
THRESHOLD = 1000


def init_file() -> wave.Wave_write:
    wave_file = wave.open(REC_FILE, "wb")
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(2)
    wave_file.setframerate(RATE)
    return wave_file


def listen() -> Generator[None, None, None]:
    # Open the default microphone and start recording
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    wave_file = init_file()
    # Continuously read the microphone input and check the amplitude
    last_positive = datetime.min
    print("Listening")
    while True:
        # Read the microphone input
        data = stream.read(CHUNK)

        # Convert the audio data to a numpy array and compute the amplitude
        audio_data = np.frombuffer(data, np.int16)
        amplitude = np.abs(audio_data).mean()

        # If the amplitude is above the threshold, write the audio data to the file
        if amplitude > THRESHOLD:
            last_positive = datetime.now()
        if datetime.now() - last_positive < timedelta(seconds=1):
            wave_file.writeframes(data)

        # Stop the recording and save the file when the user is done speaking
        if datetime.now() - last_positive > timedelta(seconds=2) and last_positive != datetime.min:
            stream.stop_stream()
            wave_file.close()
            yield
            print("Listening")
            last_positive = datetime.min
            wave_file = init_file()
            stream.start_stream()

