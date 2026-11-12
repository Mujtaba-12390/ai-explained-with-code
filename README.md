# AI, Explained With Code

Small, runnable Python scripts that go with my Medium stories. Each one is a single file you can read in a few minutes and run in seconds.

| Script | Story | What it shows |
|---|---|---|
| [`token_meter.py`](token_meter.py) | *Your AI Chat Charges You for Every Mile You’ve Already Driven* | Why message 40 of a chat costs ~7× message 1, what hidden reasoning tokens add, and how prompt caching cuts the bill |
| [`rag_without_ai.py`](rag_without_ai.py) | *I Built a RAG System With No AI. It Broke in the Same Places Yours Does.* | A BM25 retriever in plain Python, and the four ways retrieval fails before a model ever sees the question |
| [`best_of_n.py`](best_of_n.py) | *Six Ways AI Launches Make a Model Look Smarter Than It Is* | How pass@k, majority voting and best-of-many runs change a benchmark score without changing the model |
| [`idempotency.py`](idempotency.py) | *AI Agents Keep Failing in Ways My Architecture Textbook Already Named* | How a retrying agent refunds a customer three times, and the idempotency key that stops it |

## Run it

```bash
python token_meter.py
python rag_without_ai.py
python idempotency.py

pip install -r requirements.txt   # numpy, only needed for best_of_n.py
python best_of_n.py
```

Tested with Python 3.12. `token_meter.py`, `rag_without_ai.py` and `idempotency.py` use only the standard library.

## Notes

- Prices in `token_meter.py` are illustrative ($3 / $15 per million input/output tokens). Change them to match the model you use.
- `best_of_n.py` uses a fixed random seed, so you'll get the same numbers as the article.

## Licence

MIT. Use it, change it, share it.
