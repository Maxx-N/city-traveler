from constants import MODEL, openai


def find_out_the_main_spoken_language_in_city(
    city: str, model: str = MODEL
) -> str | None:
    system_prompt = """You are a helpful assistant that finds out the main language spoken in a city.
    Respond with the name of the language only, without any additional text."""
    user_prompt = f"What is the main language spoken in {city}?"
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content


def translate_text(text: str, target_language: str, model: str = MODEL) -> str | None:
    system_prompt = f"""You are a helpful assistant that translates text into {target_language}.
    Respond with the translated text only, without any additional text.
    The response should contain 2000 characters at most.
    Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown."""
    user_prompt = f"Translate the following text into {target_language}, in 2000 characters or less:\n\n{text}"
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return (
        response.choices[0].message.content[:4096]
        if response.choices[0].message.content
        else None
    )


def translate_text_into_city_language(text: str, city: str) -> str | None:
    """Translates the given text into the main language spoken in the specified city."""
    print("TOOL CALL: translate_text_into_city_language")
    main_language = find_out_the_main_spoken_language_in_city(city)
    if not main_language:
        return None
    if main_language.lower() == "english":
        return text
    translated_text = translate_text(text, main_language)
    return translated_text
