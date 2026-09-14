from helpers.summarizer import summarize_wikipedia_page
from helpers.translator import translate_text_into_city_language


def get_function_name_and_description(func) -> tuple[str, str | None]:
    name = func.__name__
    description = func.__doc__ or None
    return (name, description)


def turn_function_into_tool(func, required_parameters):
    name, description = get_function_name_and_description(func)

    function_dictionary = {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": required_parameters,
            "required": list(required_parameters.keys()),
            "additionalProperties": False,
        },
    }

    return {"type": "function", "function": function_dictionary}


def define_parameters():
    summarize_wikipedia_page_params = {
        "city": {
            "type": "string",
            "description": "The city for which to summarize the Wikipedia page.",
        }
    }
    translate_text_into_city_language_params = {
        "text": {
            "type": "string",
            "description": "The text to translate into the main language spoken in the specified city.",
        },
        "city": {
            "type": "string",
            "description": "The city whose main language will be used for translation.",
        },
    }
    return summarize_wikipedia_page_params, translate_text_into_city_language_params


def define_tools():
    summarize_wikipedia_page_params, translate_text_into_city_language_params = (
        define_parameters()
    )

    summarize_wikipedia_page_tool = turn_function_into_tool(
        func=summarize_wikipedia_page,
        required_parameters=summarize_wikipedia_page_params,
    )

    translate_text_into_city_language_tool = turn_function_into_tool(
        func=translate_text_into_city_language,
        required_parameters=translate_text_into_city_language_params,
    )

    return [summarize_wikipedia_page_tool, translate_text_into_city_language_tool]
