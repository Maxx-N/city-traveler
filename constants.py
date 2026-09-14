# MODEL = "gpt-5.6-luna"
# TTS_MODEL = "tts-1"

import os

from openai import OpenAI

MODEL = "gpt-4o-mini"
TTS_MODEL = "gpt-4o-mini-tts"

HAS_REASONING_EFFORT = False

RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "city_info",
        "schema": {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "translated_summary": {"type": "string"},
            },
            "required": ["summary", "translated_summary"],
        },
    },
}

openai_api_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=openai_api_key)
