"""A tiny RAG retriever with no AI model at all: BM25 in pure Python.

The point: most RAG failures happen before the language model ever sees
the question. Run it and watch the three failures.
"""
import math
import re
from collections import Counter

DOCS = {
    "handbook-2024#remote": "Remote work policy 2024. Employees may work remotely up to two days per week with manager approval.",
    "handbook-2026#remote": "Remote work policy 2026. Employees may work remotely up to four days per week. No approval is needed for up to two days.",
    "handbook-2026#leave": "Annual leave. Full-time employees receive 25 days of paid leave per year, plus public holidays.",
    "handbook-2026#expenses": "Expenses. Submit receipts within 30 days. Meals are reimbursed up to 40 dollars per day when travelling.",
    "handbook-2026#laptop-a": "Equipment. Every employee receives a laptop on day one. If the laptop is lost or stolen, report it to IT within",
    "handbook-2026#laptop-b": "24 hours. A replacement is issued within three working days. Repeated losses are reviewed by your manager.",
    "handbook-2026#security": "Security. Use the company VPN on public networks. Never share passwords. Enable two-factor authentication.",
}

def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())

class BM25:
    def __init__(self, docs, k1=1.5, b=0.75):
        self.ids = list(docs)
        self.tf = {i: Counter(tokens(t)) for i, t in docs.items()}
        self.len = {i: sum(c.values()) for i, c in self.tf.items()}
        self.avg = sum(self.len.values()) / len(self.len)
        df = Counter(w for c in self.tf.values() for w in c)
        n = len(docs)
        self.idf = {w: math.log(1 + (n - d + 0.5) / (d + 0.5)) for w, d in df.items()}
        self.k1, self.b = k1, b

    def score(self, query, doc_id):
        tf, s = self.tf[doc_id], 0.0
        for w in tokens(query):
            if w not in tf:
                continue
            f = tf[w]
            norm = f + self.k1 * (1 - self.b + self.b * self.len[doc_id] / self.avg)
            s += self.idf[w] * f * (self.k1 + 1) / norm
        return s

    def search(self, query, k=2):
        ranked = sorted(self.ids, key=lambda i: self.score(query, i), reverse=True)
        return [(i, round(self.score(query, i), 2)) for i in ranked[:k]]

index = BM25(DOCS)
QUESTIONS = [
    ("1. a question that works", "How many days of paid leave do I get?"),
    ("2. same meaning, different words", "Can I WFH on Fridays?"),
    ("3. the answer split across chunks", "How fast do I get a new laptop if mine is stolen?"),
    ("4. two versions of the truth", "How many days per week can I work remotely?"),
]
for label, q in QUESTIONS:
    print(f"\n{label}\n   Q: {q}")
    for doc_id, s in index.search(q):
        print(f"   {s:>5}  {doc_id}")
