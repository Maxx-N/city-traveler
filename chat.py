import json

import gradio as gr

from constants import HAS_REASONING_EFFORT, MODEL, RESPONSE_FORMAT, openai
from helpers.image_fetcher import fetch_wikipedia_image
from helpers.summarizer import summarize_wikipedia_page
from helpers.talker import talker
from helpers.translator import translate_text_into_city_language
from prompt import define_system_prompt
from tools import define_tools


def handle_tool_calls_and_return_city(message):
    responses = []
    city = None
    for tool_call in message.tool_calls:
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)
        if tool_args.get("city") and city is None:
            city = tool_args.get("city")
        tool = globals()[tool_name]
        result = tool(**tool_args)
        responses.append(
            {
                "role": "tool",
                "content": result,
                "tool_call_id": tool_call.id,
            }
        )
    return responses, city


def chat(user_message, history):
    reasoning_kwargs = {"reasoning_effort": None} if HAS_REASONING_EFFORT else {}
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    print("MESSAGE:", user_message)
    print("HISTORY:", history)
    system_prompt = define_system_prompt()
    messages = (
        [{"role": "system", "content": system_prompt}]
        + history
        + [{"role": "user", "content": user_message}]
    )
    tools = define_tools()
    response = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        **reasoning_kwargs,
        response_format=RESPONSE_FORMAT,
    )
    city = None
    while response.choices[0].finish_reason == "tool_calls":
        assistant_message = response.choices[0].message
        tool_responses, tool_city = handle_tool_calls_and_return_city(assistant_message)
        if not city and tool_city:
            city = tool_city
        messages.append(assistant_message)
        messages.extend(tool_responses)
        response = openai.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            **reasoning_kwargs,
            response_format=RESPONSE_FORMAT,
        )
    result = response.choices[0].message.content
    dict_result = json.loads(result) if result else {}

    summary = dict_result.get("summary", "")
    translated_summary = dict_result.get("translated_summary", "")

    history.extend(
        [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": summary},
        ]
    )

    image = fetch_wikipedia_image(city) if city else None
    voice = talker(translated_summary) if translated_summary else None

    return history, translated_summary, image, voice, ""


def chat_with_ui():
    full_height = 800
    fill_css = """
    .fill-pane { flex: 1 1 0 !important; min-height: 0 !important; }
    """

    with gr.Blocks() as ui:
        with gr.Row(height=full_height, scale=1):
            with gr.Column():
                chatbot = gr.Chatbot(
                    label="City Info Chatbot", height="100%", elem_classes="fill-pane"
                )
                user_input_textbox = gr.Textbox(
                    label="Ask about a city",
                    placeholder="Type your question here...",
                    autofocus=True,
                    lines=1,
                    max_lines=1,
                )
            with gr.Column():
                image_output = gr.Image(
                    label="Wikipedia Image",
                    height="100%",
                    interactive=False,
                    elem_classes="fill-pane",
                )
                translated_markdown = gr.Markdown(
                    label="Translated Summary", height="100%", elem_classes="fill-pane"
                )
                audio_output = gr.Audio(
                    label="Translated Summary Audio", interactive=False, autoplay=True
                )

        user_input_textbox.submit(
            fn=chat,
            inputs=[user_input_textbox, chatbot],
            outputs=[
                chatbot,
                translated_markdown,
                image_output,
                audio_output,
                user_input_textbox,
            ],
        )

    ui.launch(inbrowser=True, css=fill_css)
