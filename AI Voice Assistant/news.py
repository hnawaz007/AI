import requests
#from newsapi import NewsApiClient
from newsapi.newsapi_client import NewsApiClient

# category
#Find sources that display news of this category. Possible options: business entertainment general health science sports technology. Default: all categories.
api_key='your_api_key_goes_here'
newsapi = NewsApiClient(api_key=api_key)

def get_article_contents(articles):
    """Extracts the content from a list of NewsAPI article dicts."""
    contents = []
    for article in articles:
        if article.get("description"):  # only if content exists
            contents.append(article["description"])
    return contents

#
async def get_top_news(country: str = "us", num_headlines: int = 5, api_key: str = None, **kwargs) -> str:
    try:
        top_headlines = newsapi.get_top_headlines(
            country='us',
            page_size=5
        )
        data = top_headlines

        articles = data.get("articles", [])
        if not articles:
            print("No news headlines found.")
        summary_lines = []
        for art in articles:
            title = art.get("title")
            desc = art.get("description")
            if title and desc:
                summary_lines.append(f"• {title}: {desc}")
            elif title:
                summary_lines.append(f"• {title}")

        summary = "Here are today's top news headlines:\n" + "\n".join(summary_lines)
        return summary
    except Exception as e:
        print(f"Failed to fetch news: {e}")
        return "Sorry, I could not fetch the top news right now."

#
VALID_CATEGORIES = {"business", "entertainment", "general", "health", "science", "sports", "technology"}
TOPIC_MAP = {
    "tech": "technology", "technology": "technology", "science": "science",
    "sports": "sports", "health": "health", "business": "business",
    "entertainment": "entertainment", "general": "general",
}

async def get_more_articles(topic: str, num_headlines: int = 5, api_key: str = None, **kwargs) -> str:
    try:
        category = TOPIC_MAP.get(topic.lower(), topic.lower())
        if category not in VALID_CATEGORIES:
            return f"Sorry, I don't have a news category for {topic}. Try technology, sports, business, health, science, or entertainment."
        top_headlines = newsapi.get_top_headlines(
            page_size=5,
            category=category
        )
        data = top_headlines

        articles = data.get("articles", [])
        if not articles:
            print("No news headlines found.")
        summary_lines = []
        for art in articles:
            title = art.get("title")
            desc = art.get("description")
            if title and desc:
                summary_lines.append(f"• {title}: {desc}")
            elif title:
                summary_lines.append(f"• {title}")

        summary = f"Here are today's top {topic} news headlines:\n" + "\n".join(summary_lines)
        return summary
    except Exception as e:
        print(f"Failed to fetch news: {e}")
        return f"Sorry, I could not fetch news for {topic}."

#
