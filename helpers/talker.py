from constants import TTS_MODEL, openai


def talker(text: str, model: str = TTS_MODEL) -> bytes | None:
    """Generates speech from the given text using OpenAI's TTS model."""
    response = openai.audio.speech.create(
        model=model, voice="coral", input=text[:4096], speed=1
    )
    return response.content
