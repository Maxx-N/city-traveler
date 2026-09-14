"""
GENERAL CONCEPT:
- The user enters a city
- The LLM:
    - Uses a tool to scrap the English Wikipedia page
    - If scraping the Wikipedia page worked:
        - Uses a tool to get the first Wikipedia image -> Wikipedia Image
        - Uses a subagent to summarize the Wikipedia page in a concise, structured and compelling way -> Summary
        - Uses a subagent to find out the main language spoken in the city
        - Uses a subagent to get a summary translated in the city language (if it's not English) -> Translated Summary
        - Uses a subagent to get an audio summary (= audio version of the Translated Summary if it exists / of the Summary if not) -> Audio Summary
        - Displays:
            * the Wikipedia Image (if exists)
            * the Translated Summary (if exists)
            * the Summary in markdown
            * an audio player with the Audio Summary
    - If scraping the Wikipedia page failed:
        - Displays a message to the user, saying so
"""

from dotenv import load_dotenv

load_dotenv()

from chat import chat_with_ui

chat_with_ui()
