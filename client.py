"""Trie Prefix Keyword Matcher.
100% Python Standard Library.
"""
from typing import Dict, Any, List, Optional

class TrieNode:
    __slots__ = ('children', 'is_end', 'metadata')
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end: bool = False
        self.metadata: Optional[Any] = None

class TriePrefixKeywordMatcher:
    """In-memory Trie for multi-keyword search, prefix routing, and entity extraction."""
    def __init__(self):
        self.root = TrieNode()
        self.word_count = 0
        self.node_count = 1

    def insert(self, word: str, metadata: Optional[Any] = None) -> None:
        curr = self.root
        for char in word:
            if char not in curr.children:
                curr.children[char] = TrieNode()
                self.node_count += 1
            curr = curr.children[char]
        if not curr.is_end:
            self.word_count += 1
        curr.is_end = True
        curr.metadata = metadata

    def insert_words(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        count = 0
        for item in items:
            w = item.get("word", "").strip()
            if w:
                self.insert(w, item.get("metadata"))
                count += 1
        return {"inserted_count": count, "total_words": self.word_count, "total_nodes": self.node_count}

    def search_prefix(self, prefix: str, max_results: int = 10) -> List[Dict[str, Any]]:
        curr = self.root
        for char in prefix:
            if char not in curr.children:
                return []
            curr = curr.children[char]

        results = []
        def _dfs(node: TrieNode, current_str: str):
            if len(results) >= max_results:
                return
            if node.is_end:
                results.append({"word": current_str, "metadata": node.metadata})
            for char, next_node in sorted(node.children.items()):
                _dfs(next_node, current_str + char)

        _dfs(curr, prefix)
        return results

    def find_all_matches(self, text: str) -> List[Dict[str, Any]]:
        matches = []
        n = len(text)
        for i in range(n):
            curr = self.root
            j = i
            while j < n and text[j] in curr.children:
                curr = curr.children[text[j]]
                j += 1
                if curr.is_end:
                    matches.append({
                        "word": text[i:j],
                        "start": i,
                        "end": j,
                        "metadata": curr.metadata
                    })
        return matches

    def get_trie_stats(self) -> Dict[str, Any]:
        return {
            "total_words": self.word_count,
            "total_nodes": self.node_count
        }
