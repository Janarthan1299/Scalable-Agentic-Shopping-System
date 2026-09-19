import re
from pathlib import Path
from typing import Any


def _chunks() -> list[dict[str, str]]:
    directory = Path(__file__).parents[2] / "data" / "knowledge_base"
    return [{"source": path.name, "text": path.read_text().strip()} for path in directory.glob("*.txt")]


def rag_search(query: str) -> dict[str, Any]:
    terms = set(re.findall(r"[a-z0-9]+", query.lower()))
    ranked = []
    for chunk in _chunks():
        score = len(terms.intersection(set(re.findall(r"[a-z0-9]+", chunk["text"].lower()))))
        ranked.append((score, chunk))
    ranked.sort(key=lambda item: item[0], reverse=True)
    selected = [chunk for score, chunk in ranked if score > 0][:3] or [ranked[0][1]]
    return {"query": query, "matches": selected, "answer": " ".join(item["text"] for item in selected)}
