"""Why an agent that retries can refund a customer twice, and the one-line fix."""
import uuid

class PaymentAPI:
    def __init__(self):
        self.refunds = []          # what actually happened
        self.seen = {}             # idempotency key -> result

    def refund(self, order, amount, key=None):
        if key and key in self.seen:
            return self.seen[key]  # same request again: return the old result
        self.refunds.append((order, amount))
        result = f"refunded {amount} on {order}"
        if key:
            self.seen[key] = result
        return result

def agent_refund(api, order, amount, use_key):
    key = str(uuid.uuid4()) if use_key else None   # one key per intended action
    for attempt in range(3):
        api.refund(order, amount, key)
        # the response is lost on the first two attempts (a timeout),
        # so the agent thinks it failed and tries again
        if attempt == 2:
            return

for use_key in (False, True):
    api = PaymentAPI()
    agent_refund(api, "order-1042", 59.99, use_key)
    print(f"idempotency key: {use_key!s:<5} -> refunds issued: {len(api.refunds)}")
