# 📚 study-notes.md

## Lecture 02: What a Harness Actually Is

---

## 🧭 Overview

> **"A prompt file is not a harness."**

A **harness** is everything in the engineering infrastructure *outside* the model weights. It is the structured environment that determines how much of a model's raw capability actually gets realized in practice.

A harness consists of **five subsystems**:

| # | Subsystem | Core Responsibility |
|---|-----------|-------------------|
| 1 | **Instructions** | Tell the agent what the project is and how to behave |
| 2 | **Tools** | Give the agent the ability to act (shell, files, tests) |
| 3 | **Environment** | Make the runtime state reproducible and self-describing |
| 4 | **State** | Track progress across sessions for long-running tasks |
| 5 | **Feedback** | Let the agent verify its own work with executable checks |

---

## 🏗️ The Core Analogy

Imagine being a new engineer dropped into a project with no help.
Most of your time could go to **orientation**, not **problem-solving**.

An AI agent faces the same problem. It can only see what you put in front of it.

> **"The repo IS the spec."** — OpenAI
Everything the agent cannot see, for all practical purposes, does not exist.

---

## 🧩 The Five Subsystems — In Detail

### 1. 📋 Instruction Subsystem
**File:** `AGENTS.md` or `CLAUDE.md`

Should contain:
- Project overview and purpose
- Tech stack and versions
- First-run commands
- Hard constraints (non-negotiable rules)
- Links to deeper docs

> **"Give a map, not a manual."**
> ~100 lines is the sweet spot. If it doesn't fit, split into a `docs/` directory.

---

### 2. 🛠️ Tool Subsystem
- Give the agent **sufficient** tool access
- Don't disable the shell for vague "security reasons" — if it can't run `pip install`, it can't function
- Follow the **principle of least privilege** — don't open *everything* either

---

### 3. 🌍 Environment Subsystem
Make the environment **self-describing and reproducible**:

| What | How |
|------|-----|
| Dependency locking | `pyproject.toml` / `package.json` |
| Runtime version pinning | `.nvmrc` / `.python-version` |
| Full reproducibility | Docker / devcontainers |

---

### 4. 🗂️ State Subsystem
Long tasks **require** progress tracking. Use a simple `PROGRESS.md`:

```markdown
## Done
- [x] Set up project scaffold
- [x] Implemented auth module

## In Progress
- [ ] Dashboard component (50% complete)

## Blocked
- [ ] Payment integration — waiting on API keys
```

> **Rule:** Update before each session ends. Read at the start of the next.

---

### 5. ✅ Feedback Subsystem
> **Highest ROI of all five subsystems.**

List explicit verification commands directly in `AGENTS.md`:

```yaml
Verification commands:
  - Tests:       pytest tests/ -x
  - Type check:  mypy src/ --strict
  - Lint:        ruff check src/
  - Full check:  make check  # runs all of the above
```

> **Why this matters:** Anthropic found that agents confidently praise their own work.
> The fix is to separate *"the one who does the work"* from *"the one who checks the work."*

---

## 🧪 Measuring What Actually Matters

Remove one subsystem at a time, keep the model fixed, measure the performance drop.
Biggest drop = highest marginal value right now.

> ⚠️ Ablation shows *what's valuable* — not *where the bottleneck is*.
> For root cause, read your failure logs and attribute them first.

---

## Key Takeaways

- **All five subsystems are required.** Missing one always shows.
- **Feedback first** — lowest effort, highest return. Get verification commands in place before anything else.
- **Harness rots.** Audit it like you audit technical debt.
- Agents praise their own work — separate the doer from the checker.
- A better harness beats a better model. Optimize the harness first.
