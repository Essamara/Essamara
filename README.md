# Llama.cpp News Plugin

This project is a Python-based plugin for `llama.cpp` that allows a local Large Language Model (LLM) to fetch and summarize the latest news on a topic you provide. It uses the `llama.cpp` server's OpenAI-compatible API and its function-calling/tool-use feature.

## How It Works

1.  **User Input**: When you run the main script, it will prompt you to enter a news topic (e.g., "London" or "AI development").
2.  **`news_plugin.py`**: This script takes your input and sends a prompt to the LLM asking for a news summary on that topic. It also defines a `get_news` tool that the LLM can use.
3.  **Function Call**: The LLM, running on the `llama.cpp` server, recognizes that it needs to use the `get_news` tool. It sends a response back to the script indicating that it wants to call the function with your chosen topic.
4.  **`get_news.py`**: The main script then calls the `get_news()` function, which makes an API request to [The News API](https://thenewsapi.com) to fetch the latest articles related to your topic.
5.  **Summarization**: The fetched news is sent back to the LLM as the result of the tool call. The LLM then uses this information to generate a concise summary, which is printed to the console.

## Setup and Usage

Follow these steps to set up and run the news plugin.

### 1. Start the `llama.cpp` Server

You need to have a local `llama.cpp` server running with a model that supports function calling.

-   Follow the official `llama.cpp` server documentation to build and run the server: [https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
-   Start the server. An example command might look like this:
    ```bash
    ./server -m models/gguf-model-q4_k_m.gguf -c 4096 --host 0.0.0.0 --port 8080
    ```
-   Make sure the server is running and accessible at `http://localhost:8080`.

### 2. Get a News API Key

This plugin uses [The News API](https://thenewsapi.com) to fetch news.

1.  Go to [https://thenewsapi.com/register](https://thenewsapi.com/register) and sign up for a free account.
2.  After signing up, you will get a free API key.

### 3. Set Up the Python Environment

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set the News API key as an environment variable:**
    -   **Linux/macOS:**
        ```bash
        export NEWS_API_KEY="YOUR_API_KEY_HERE"
        ```
    -   **Windows (Command Prompt):**
        ```bash
        set NEWS_API_KEY="YOUR_API_KEY_HERE"
        ```
    -   **Windows (PowerShell):**
        ```bash
        $env:NEWS_API_KEY="YOUR_API_KEY_HERE"
        ```
    Replace `"YOUR_API_KEY_HERE"` with the actual key you obtained from The News API.

### 4. Run the Plugin

Once the `llama.cpp` server is running and your environment is set up, you can run the plugin:

```bash
python news_plugin.py
```

The script will prompt you to enter a topic. After you provide a topic, it will interact with the local LLM to fetch and display a summary of the latest news.