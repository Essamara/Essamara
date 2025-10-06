import os
from openai import OpenAI
from get_news import get_news

# Point to the local server
client = OpenAI(base_url="http://localhost:8080/v1", api_key="not-needed")

# --- 1. Define the updated get_news tool ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_news",
            "description": "Get the latest news articles on a specific topic from a global feed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The topic to search for, e.g., 'Paris' or 'London'.",
                    },
                    "language": {
                        "type": "string",
                        "description": "The 2-letter language code for the news, e.g., 'en' for English.",
                    },
                },
                "required": ["query"],
            },
        },
    }
]

def run_conversation():
    """
    Prompts the user for a topic and then starts a conversation with the model to get a news summary.
    """
    # --- 2. Get user input for the news topic ---
    topic = input("Enter the news topic you want to search for (e.g., 'Paris', 'London', 'AI development'): ")
    if not topic.strip():
        print("No topic entered. Exiting.")
        return

    # --- 3. Create the initial message ---
    messages = [
        {
            "role": "user",
            "content": f"What's the latest news on {topic}? Please summarize the top 3 articles for me.",
        }
    ]

    # --- 4. Send the message and tools to the model ---
    print(f"\nAsking the model for the latest news on '{topic}'...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", # Model name doesn't matter for local server
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # --- 5. Check if the model wants to call the tool ---
    if tool_calls:
        print("Model wants to fetch the news. Calling the tool...")
        tool_call = tool_calls[0]
        function_name = tool_call.function.name

        if function_name == "get_news":
            # --- 6. Call the get_news function ---
            api_key = os.environ.get("NEWS_API_KEY", "YOUR_API_KEY_HERE")
            if api_key == "YOUR_API_KEY_HERE":
                print("\nERROR: Please set your NEWS_API_KEY environment variable.")
                return

            import json
            tool_args = json.loads(tool_call.function.arguments)
            query = tool_args.get("query", topic) # Use the topic from user input

            print(f"Fetching news for query: '{query}'")
            news_results = get_news(api_key=api_key, query=query, limit=3)

            # --- 7. Send the news back to the model for summarization ---
            print("News received. Asking model to summarize...")
            messages.append(response_message)
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": news_results,
                }
            )

            second_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )

            # --- 8. Print the final summary ---
            print("\n--- News Summary ---")
            print(second_response.choices[0].message.content)
            print("--------------------\n")
        else:
            print(f"Error: Model tried to call an unknown function: {function_name}")

    else:
        # --- Handle cases where the model responds directly ---
        print("\n--- Model Response ---")
        print(response_message.content)
        print("----------------------\n")


if __name__ == "__main__":
    run_conversation()