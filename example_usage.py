"""Example usage for GenPark Trie Prefix Keyword Matcher."""
from client import TriePrefixKeywordMatcher

def main():
    trie = TriePrefixKeywordMatcher()
    print("Ingesting prompt keywords into Trie...")
    trie.insert_words([
        {"word": "weather", "metadata": {"handler": "weather_agent"}},
        {"word": "web search", "metadata": {"handler": "search_agent"}},
        {"word": "database query", "metadata": {"handler": "sql_agent"}},
        {"word": "data analysis", "metadata": {"handler": "python_eval_agent"}}
    ])

    print("Searching prefix 'data'...")
    results = trie.search_prefix("data")
    for r in results:
        print(f" - {r['word']} -> {r['metadata']}")

    print("
Scanning text for keyword matches...")
    text = "Please run a web search and do some data analysis on the results."
    matches = trie.find_all_matches(text)
    for m in matches:
        print(f"Match: '{m['word']}' at index [{m['start']}:{m['end']}] -> {m['metadata']}")

if __name__ == "__main__":
    main()
