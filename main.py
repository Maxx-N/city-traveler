"""
GENERAL CONCEPT:
- The user enters a city
- The LLM:
    - Uses a subagent to find the relevant Wikipedia page
    - If there is a relevant Wikipedia page:
        - Uses a tool to get the first Google image -> Google Image
        - Uses a tool to scrap the Wikipedia page
        - Uses a subagent to summarize the Wikipedia page in a concise, structured and compelling way -> Summary
        - Uses a subagent to find out the main language spoken in the city
        - Uses a subagent to get a summary translated in the city language (if it's not English) -> Translated Summary
        - Uses a subagent to get an audio summary (= audio version of the Translated Summary if it exists / of the Summary if not) -> Audio Summary
        - Displays the Google Image (if exists), the Translated Summary (if exists) + the Summary in markdown, and an audio player with the Audio Summary
    - If there is no relevant Wikipedia page:
        - Displays a message to the user, saying so
"""
