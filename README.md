# What is this?

Speak with gpt chat model, with your voice.

# How does it work?

```
speech-recognition -> gptchat -> text-to-speech.
```

- whisper model does speech-to-text
- gpt chat does gpt chat...
- google-text-to-speech does text-to-speech

# How do I use it?

You'll need the gpt chat token. Get if from the web cookie named `__Secure-next-auth.session-token`.

```
# install poetry
pip install poetry

# install poetry requirements
poetry install

# run
poetry run python gpt_speak/main.py --token <YOUR_TOKEN>
```

