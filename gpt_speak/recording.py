from datetime import datetime, timedelta
from numpy.lib.shape_base import array_split
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

# Open the default microphone and start recording
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Create a Wave_write object to save the recorded audio to a file
wf = wave.open(REC_FILE, "wb")
wf.setnchannels(CHANNELS)
wf.setsampwidth(2)
wf.setframerate(RATE)

def listen() -> None:
    # Continuously read the microphone input and check the amplitude
    start = datetime.now()
    last_positive = datetime.min
    while True:
        # Read the microphone input
        data = stream.read(CHUNK)

        # Convert the audio data to a numpy array and compute the amplitude
        audio_data = np.frombuffer(data, np.int16)
        amplitude = np.abs(audio_data).mean()
        print("Aplitude:", amplitude)

        # If the amplitude is above the threshold, write the audio data to the file
        if amplitude > THRESHOLD:
            last_positive = datetime.now()
        if datetime.now() - last_positive < timedelta(seconds=1):
            wf.writeframes(data)

        # Stop the recording and save the file when the user is done speaking
        if datetime.now() - start > timedelta(seconds=10):
            break

    # Close the stream and file
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()
