"""Why the 40th message in a chat costs more than the first.

Every turn, a chat API re-sends the whole conversation so far as input.
This script prices a conversation turn by turn with illustrative numbers.
"""

PRICE_IN = 3.00     # dollars per million input tokens (illustrative)
PRICE_OUT = 15.00   # dollars per million output tokens (illustrative)
CACHE_READ = 0.10   # cached input billed at 10% of the input price (illustrative)

SYSTEM = 1_500      # system prompt + tool definitions, sent every turn
USER = 150          # each new user message
REPLY = 400         # each visible assistant reply
THINK = 2_000       # hidden reasoning tokens per reply (billed as output)


def conversation(turns, think=0, cached=False):
    history = 0                     # tokens of past messages
    rows = []
    for t in range(1, turns + 1):
        fresh = USER
        reused = SYSTEM + history   # everything the model has already seen
        if cached:
            cost_in = (fresh * PRICE_IN + reused * PRICE_IN * CACHE_READ) / 1e6
        else:
            cost_in = (fresh + reused) * PRICE_IN / 1e6
        cost_out = (REPLY + think) * PRICE_OUT / 1e6
        rows.append((t, fresh + reused, cost_in + cost_out))
        history += USER + REPLY     # reasoning tokens are not kept in history
    return rows


if __name__ == "__main__":
    plain = conversation(40)
    first, last = plain[0][2], plain[-1][2]
    total = sum(r[2] for r in plain)
    print(f"turn 1 : {plain[0][1]:>6,} input tokens  ${first:.4f}")
    print(f"turn 10: {plain[9][1]:>6,} input tokens  ${plain[9][2]:.4f}")
    print(f"turn 40: {plain[-1][1]:>6,} input tokens  ${last:.4f}")
    print(f"turn 40 costs {last / first:.1f}x turn 1")
    print(f"40-turn chat total: ${total:.2f}")
    half = sum(r[2] for r in plain[:20])
    print(f"share of the bill spent in the last 20 turns: {1 - half / total:.0%}")

    for label, rows in [("with hidden reasoning", conversation(40, think=THINK)),
                        ("with prompt caching", conversation(40, cached=True)),
                        ("reasoning + caching", conversation(40, think=THINK, cached=True))]:
        print(f"{label:<22}: ${sum(r[2] for r in rows):.2f}")

    # what the same 40 questions cost as 40 fresh one-question chats
    fresh = 40 * conversation(1)[0][2]
    print(f"40 separate one-turn chats: ${fresh:.2f}")
