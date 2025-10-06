import requests
import os

def get_news(api_key: str, query: str = "world news", language: str = "en", limit: int = 5, published_after: str = None, published_before: str = None) -> str:
    """
    Fetches the latest news from The News API's 'all' endpoint for more recent results.

    Args:
        api_key: Your API key for The News API.
        query: The search query for news articles.
        language: The language to fetch news in (e.g., 'en', 'de').
        limit: The number of articles to return.

    Returns:
        A formatted string of news headlines and snippets, or an error message.
    """
    # Using the '/all' endpoint to get more recent, less curated news
    api_url = f"https://api.thenewsapi.com/v1/news/all?api_token={api_key}&search={query}&language={language}&limit={limit}"
    if published_after:
        api_url += f"&published_after={published_after}"
    if published_before:
        api_url += f"&published_before={published_before}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        news_data = response.json()

        if not news_data.get("data"):
            return "No news articles found."

        formatted_news = ""
        for article in news_data["data"]:
            title = article.get("title", "No Title")
            snippet = article.get("snippet", "No Snippet Available")
            source = article.get("source", "No Source")
            formatted_news += f"Title: {title}\nSource: {source}\nSnippet: {snippet}\n\n"

        return formatted_news.strip()

    except requests.exceptions.RequestException as e:
        return f"Error fetching news: {e}"
    except KeyError:
        return "Error: Unexpected format in API response."

if __name__ == '__main__':
    # You can run this script directly to test it.
    # Make sure to set your API key in an environment variable named 'NEWS_API_KEY'
    api_key = os.environ.get("NEWS_API_KEY", "XNLDKFYxf91IIsVYaHNAJlQDIoASIjHLIedPn0Nx")
    if api_key == "YOUR_API_KEY_HERE":
        print("Please set your NEWS_API_KEY environment variable or replace 'YOUR_API_KEY_HERE' in the script.")
    else:
        # Fetch latest news about 'AI development'
        news = get_news(api_key, query="AI development", language="en")
        print(news)
