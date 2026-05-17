import pywhatkit as kit

async def play_youtube(query: str) -> str:
    """
    Search YouTube and play the first matching video in the browser.

    Args:
        query (str): The song name or video title.

    Returns:
        str: A message confirming the action.
    """
    try:
        kit.playonyt(query)
        return f"Playing '{query}' on YouTube."
    except Exception as e:
        return f"Failed to play '{query}'. Error: {e}"

#
# if __name__ == "__main__":
#     result = play_youtube("coke studio tu jhoom")
#     print(result)