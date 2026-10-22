"""MCP Stdio Server for Trie Prefix Keyword Matcher.
100% Python Standard Library.
"""
import sys
import json
from client import TriePrefixKeywordMatcher

trie = TriePrefixKeywordMatcher()

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-trie-prefix-keyword-matcher-skill", "version": "1.0.1"},
            "capabilities": {"tools": {}}
        }
        send_response(req_id, res)
    elif method == "tools/list":
        tools = [
            {
                "name": "insert_words",
                "description": "Insert keyword entries and optional metadata into the prefix Trie",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "word": {"type": "string"},
                                    "metadata": {"type": "object"}
                                },
                                "required": ["word"]
                            }
                        }
                    },
                    "required": ["items"]
                }
            },
            {
                "name": "search_prefix",
                "description": "Find words matching a given prefix for prompt routing or auto-completion",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prefix": {"type": "string"},
                        "max_results": {"type": "integer", "default": 10}
                    },
                    "required": ["prefix"]
                }
            },
            {
                "name": "find_all_matches",
                "description": "Scan text and extract all keyword occurrences with exact character offsets",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"}
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "get_trie_stats",
                "description": "Return Trie node counts and registered word counts",
                "inputSchema": {"type": "object"}
            }
        ]
        send_response(req_id, {"tools": tools})
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "insert_words":
            out = trie.insert_words(args.get("items", []))
        elif name == "search_prefix":
            out = trie.search_prefix(args.get("prefix", ""), args.get("max_results", 10))
        elif name == "find_all_matches":
            out = trie.find_all_matches(args.get("text", ""))
        elif name == "get_trie_stats":
            out = trie.get_trie_stats()
        else:
            send_error(req_id, -32601, f"Unknown tool: {name}")
            return
        send_response(req_id, {"content": [{"type": "text", "text": json.dumps(out, indent=2)}]})

def send_response(req_id, result):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result}) + "\n")
    sys.stdout.flush()

def send_error(req_id, code, message):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
