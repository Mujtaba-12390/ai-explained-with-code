"""How 'pass@k' turns a 30% model into an 80% headline.

500 made-up problems, each with its own difficulty. The model is the same
in every row; only the way we count changes.
"""
import numpy as np

rng = np.random.default_rng(7)
N_PROBLEMS = 500
# chance the model solves each problem on a single try (most are hard)
p = rng.beta(0.6, 1.4, N_PROBLEMS)

def pass_at_k(p, k):
    # chance at least one of k independent tries is correct
    return 1 - (1 - p) ** k

for k in [1, 4, 16, 64]:
    print(f"pass@{k:<3}: {pass_at_k(p, k).mean():.1%}")

# majority vote of 32: the model answers 32 times and the most common answer wins.
# Whether that helps depends on how much the wrong answers agree with each other.
tries = rng.random((N_PROBLEMS, 32)) < p[:, None]          # which tries are right
pick = np.random.default_rng(11).integers(0, 4, tries.shape)  # wrong tries pick 1 of 4 wrong answers
right_votes = tries.sum(axis=1)
def vote(n_wrong_options):
    wrong = np.stack([((~tries) & (pick % n_wrong_options == w)).sum(axis=1)
                      for w in range(n_wrong_options)], axis=1)
    return (right_votes > wrong.max(axis=1)).mean()
print(f"majority of 32, wrong answers all agree : {vote(1):.1%}")
print(f"majority of 32, wrong answers spread 4 ways: {vote(4):.1%}")

# cherry-picking: run the benchmark 10 times, report the best run
runs = [(rng.random(N_PROBLEMS) < p).mean() for _ in range(10)]
print(f"10 runs: worst {min(runs):.1%}, median {np.median(runs):.1%}, best {max(runs):.1%}")
