from constants import MODEL, openai

from .scraper import fetch_wikipedia_page


def summarize_text(text: str, model: str = MODEL) -> str | None:
    system_prompt = """You are a helpful assistant that summarizes text in a very concise (less or equal to 2000 characters), structured and compelling way,
    ignoring text that might be navigation related. 
    Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown."""
    user_prompt = f"Summarize the following text in a very concise (less or equal to 2000 characters), structured and compelling way:\n\n{text}"
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    result = response.choices[0].message.content
    return result[:4096] if result else None


def summarize_wikipedia_page(city: str) -> str | None:
    """Fetches the Wikipedia page for a given city and summarizes its content."""
    print("TOOL CALL: summarize_wikipedia_page")
    page = fetch_wikipedia_page(city)
    if not page:
        return None
    summary = summarize_text(page)
    return summary
