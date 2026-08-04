# 📊 Lecture 01 — Exercise 1 Results: No-Harness vs Harness Run

## 🧪 Experiment Setup

- **Task Given:** `"build a 2D retro game editor"`
- **Agent:** Claude (via VS Code / Cursor)
- **Codebase:** Fresh empty directory
- **Run 1:** No harness, single vague prompt
- **Run 2:** Pending — with AGENTS.md and explicit verification

---

## 🚨 Run 1 Results — No Harness

### Failures Observed

| # | Failure | Layer | Notes |
|---|---------|-------|-------|
| 1 | Agent guessed entire scope (pygame, 20×15 grid, 10 tiles) | Task Specification | No spec = agent invents its own definition |
| 2 | Python not installed — agent had to install it mid-task | Execution Environment | Burned steps fixing env instead of building |
| 3 | No real display — forced to use dummy SDL video driver | Execution Environment | No real visual verification possible |
| 4 | Agent declared done after smoke tests only | Verification Feedback | Smoke test ≠ real correctness |
| 5 | No pre-existing tests — agent wrote inline checks on the fly | Verification Feedback | Agent invented its own definition of done |
| 6 | Next session will re-explore everything from scratch | State Management | No AGENTS.md = no persistent context |

### What the Agent Did Well
- ✅ Structured the project cleanly (`editor/`, `main.py`, `requirements.txt`)
- ✅ Self-recovered from missing Python by installing it
- ✅ Ran smoke tests proactively without being asked
- ✅ Verified save/load roundtrip with assertions
- ✅ Added `.gitignore` unprompted

### Verification Gap
```
Agent claimed completion:    ✅ Yes
Actually visually verified:  ❌ No (smoke test only)
Verification Gap:            1/1 = 100%
```

---

## ✅ Run 2 Results — With Harness

> ⏳ Pending — to be filled after Run 2

| Metric | Run 1 | Run 2 |
|--------|-------|-------|
| Scope guessed by agent | ✅ Yes | ❌ No (defined in AGENTS.md) |
| Env setup failures | 2 | ? |
| Verification gap | 100% | ? |
| Sessions needed | 1 (but incomplete) | ? |
| Core features working | ⚠️ Partial | ? |

---

## 🔑 Key Takeaway

> 5 out of 6 failures were directly fixable by harness improvements.
> The model was never the problem.

---

## 📌 Layers Reference

| # | Layer | Failure Signal |
|---|-------|---------------|
| 1 | Task Specification | Agent guesses wrong scope |
| 2 | Context Provision | Agent uses wrong patterns/conventions |
| 3 | Execution Environment | Agent fixes env instead of building |
| 4 | Verification Feedback | Agent declares done prematurely |
| 5 | State Management | Agent re-explores every new session |
