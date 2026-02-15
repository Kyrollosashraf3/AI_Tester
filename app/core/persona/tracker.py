from __future__ import annotations
from typing import Any, Dict, List
import re
import numpy as np

from app.clients.embeddings import generate_embeddings

# Question starters for detecting questions
QUESTION_STARTERS = [
    "what", "why", "how", "when", "where", "who", "which",
    "do you", "can you", "could you", "would you", "will you",
    "is it", "are there", "do they", "does it", "has it",
]

def cosine_sim_matrix(E: np.ndarray) -> np.ndarray:
    # normalize rows then dot
    norms = np.linalg.norm(E, axis=1, keepdims=True) + 1e-12
    En = E / norms
    return En @ En.T  # (n,n)


def deduplicate_questions(questions: List[str], threshold: float = 0.87) -> List[Dict[str, Dict[str, Any]]]:
    """
    Return only semantically duplicated questions (count > 1) at the end of the session.
    Each entry representative question and how many times similar versions appeared.
    Apply it in the final step of Test 
    """
    qs = [q.strip() for q in questions if q and q.strip()]
    if not qs:
        return []

    embs = np.array(generate_embeddings(qs), dtype=np.float32)  # batch :contentReference[oaicite:4]{index=4}
    S = cosine_sim_matrix(embs)

    # greedily assign each question to an existing representative
    reps: List[int] = []
    counts: List[int] = []
    rep_texts: List[str] = []

    for i, q in enumerate(qs):
        if not reps:
            reps.append(i); counts.append(1); rep_texts.append(q)
            continue

        best_rep = -1
        best_sim = -1.0
        for r_idx, r in enumerate(reps):
            sim = float(S[i, r])
            if sim > best_sim:
                best_sim, best_rep = sim, r_idx

        if best_sim >= threshold:
            counts[best_rep] += 1
        else:
            reps.append(i); counts.append(1); rep_texts.append(q)

    # output in your requested format
    return [
        {f"Quesion_{k+1}": {"Q": rep_texts[k], "n": counts[k]}}
        for k in range(len(rep_texts))
        if counts[k] > 1
    ]





def is_question(text: str) -> bool:
    """Treat the assistant message as requiring a reply if it asks something."""
    if not text or not text.strip():
        return False
    t = text.strip().lower()
    if "?" in text:
        return True
    for start in QUESTION_STARTERS:
        if t.startswith(start):
            return True
    if re.search(r":\s*$", text.strip()):
        return True
    return False


def stop_condition(text: str) -> bool:
    """Stop when assistant outputs a final Summary/closing message."""
    if not text or not text.strip():
        return False
    lower = text.lower()
    if "i've gathered all the information i need" in lower:
        return True
    if "based on our conversation" in lower:
        return True
    if "would you like to continue with" in lower:
        return True
    words = len(text.split())
    paragraphs = len([p for p in text.split("\n\n") if p.strip()])
    if words >= 80 and paragraphs >= 2:
        return True
    return False



def extract_last_question(text: str) -> str | None:
    if not text:
        return None

    matches = re.findall(r'([^?.!]*\?)', text)
    return matches[-1].strip() if matches else None
