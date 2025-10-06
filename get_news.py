import requests
import os

def get_news(api_key: str, query: str = "top stories", country: str = "us", category: str = "general", limit: int = 5) -> str:
    """
    Fetches news from The News API.

    Args:
        api_key: Your API key for The News API.
        query: The search query for news articles.
        country: The country to fetch news from (e.g., 'us', 'gb').
        category: The category of news to fetch (e.g., 'business', 'sports').
        limit: The number of articles to return.

    Returns:
        A formatted string of news headlines and snippets, or an error message.
    """
    api_url = f"https://api.thenewsapi.com/v1/news/top?api_token={api_key}&search={query}&locale={country}&limit={limit}&categories={category}"

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
            formatted_news += f"Title: {title}\nSnippet: {snippet}\n\n"

        return formatted_news.strip()

    except requests.exceptions.RequestException as e:
        return f"Error fetching news: {e}"
    except KeyError:
        return "Error: Unexpected format in API response."

if __name__ == '__main__':
    # You can run this script directly to test it.
    # Make sure to set your API key in an environment variable named 'NEWS_API_KEY'
    api_key = os.environ.get("NEWS_API_KEY", "YOUR_API_KEY_HERE")
    if api_key == "YOUR_API_KEY_HERE":
        print("Please set your NEWS_API_KEY environment variable or replace 'YOUR_API_KEY_HERE' in the script.")
    else:
        news = get_news(api_key)
        print(news)