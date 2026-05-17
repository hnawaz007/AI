from ddgs import DDGS


async def web_search(query: str, max_results: int = 3) -> str:
    """
    Perform a web search and return a summarized answer from the top results.

    Args:
        query (str): The search query string.
        max_results (int): Number of results to fetch (default: 5).

    Returns:
        str: A summarized answer combining snippets from top search results.
    """
    snippets = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            snippet = r.get("body", "")
            if snippet:
                snippets.append(snippet)

    if not snippets:
        return "I couldn't find any relevant information."

    # Combine and summarize snippets into a short answer
    summary = " ".join(snippets)
    summary = "Here’s what I found: " + summary[:600] + "..."  # limit length
    return summary

# async def web_search(query: str, max_results: int = 5) -> str:
#     snippets = []
#     with DDGS() as ddgs:
#         for r in ddgs.text(query, max_results=max_results):
#             snippet = r.get("body", "")
#             if snippet:
#                 snippets.append(snippet)

#     if not snippets:
#         return "I couldn't find any relevant information."

#     summary = " ".join(snippets)
#     summary = "Here’s what I found: " + summary[:600] + "..."
#     return summary

#
# if __name__ == "__main__":
#     query = "latest news on NVIDIA AI chips"
#     answer = web_search(query, max_results=3)
#     print(answer)