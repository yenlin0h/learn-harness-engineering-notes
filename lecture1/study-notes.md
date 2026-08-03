# 📚 Lecture 01 Summary: Strong Models Don't Mean Reliable Execution

---

## 🧠 Core Thesis

> **Model capability ≠ Execution reliability.**
> When an AI coding agent fails, the problem is usually the *environment around the model*, not the model itself.

---

## 📊 The Reality Check

- Top coding agents hit **~50–60% pass rate** on SWE-bench Verified — and that's on *ideal* tasks
- Real-world tasks (vague specs, no tests, implicit rules) push that number **even lower**
- First instinct: *"swap to a better model"* — almost always the **wrong move**

---

## 🐴 Same Horse, Different Fates (Key Experiment)

Anthropic ran the **same model** (Claude Opus 4.5) on the **same prompt** ("build a 2D retro game editor") twice:

| Run | Setup | Time | Cost | Result |
|-----|-------|------|------|--------|
| 1st | No harness | 20 min | $9 | Core features broken |
| 2nd | Full harness (planner → generator → evaluator) | 6 hrs | $200 | Fully playable game |

**The model didn't change. The harness did.**

---

## 🚧 5 Ways Agents Actually Get Stuck

1. **Vague Requirements** — "Add a search feature" tells the agent almost nothing; wrong guesses = expensive rework
2. **Implicit Conventions** — Unwritten rules (e.g., SQLAlchemy 2.0 syntax, OAuth 2.0 on all endpoints) the agent has never seen
3. **Incomplete Environment** — Missing dependencies, wrong tool versions → agent burns context on `pip install` errors instead of real work
4. **No Verification Methods** — No tests, no lint → agent *feels* done and declares completion ("context anxiety" when context runs low)
5. **Cross-Session State Loss** — Every new session re-explores the whole codebase; failure rates spike sharply on tasks over 30 minutes

---

## 🔑 Key Terminology

| Term | Definition |
|------|-----------|
| **Capability Gap** | The gulf between benchmark performance and real-world performance |
| **Harness** | Everything *outside* the model — instructions, tools, environment, state, verification |
| **Harness-Induced Failure** | Model has enough capability, but the execution environment has structural defects |
| **Verification Gap** | Agent says "done" when it isn't — the most common failure mode |
| **Diagnostic Loop** | Execute → observe failure → attribute to a harness layer → fix → re-execute |
| **Definition of Done** | A set of *verifiable-by-command* completion criteria |

---

## 🛠️ The Core Principle & What To Do About It

### ✅ When things fail — fix the harness first

**Step 1: Attribute failures to a specific layer**

Map every failure to one of the **5 harness layers**:
- Task specification
- Context provision
- Execution environment
- Verification feedback
- State management

**Step 2: Write an explicit Definition of Done**

Instead of *"add a search feature"*, write:

```markdown
Completion criteria:
- New endpoint GET /api/search?q=xxx
- Supports pagination, default 20 items
- Results include highlighted snippets
- All new code passes pytest
- Type checking passes (mypy --strict)
```

**Step 3: Add an `AGENTS.md` to your repo root**

Include:
- Tech stack & versions
- Architectural conventions
- Verification commands

> 💡 *One `AGENTS.md` file might be more effective than upgrading to a more expensive model — and that's not a joke.*

**Step 4: Build a Diagnostic Loop**

Keep a simple log per task:
- Did it succeed or fail?
- Which harness layer caused the failure?

After a few rounds, you'll see the bottleneck layer clearly.

---

## 🧪 The Million-Line Experiment (OpenAI)

- **3 engineers**, **5 months**, starting from an **empty git repo**
- Rules: only Codex writes code
- Result: **~1,000,000 lines** of agent-generated code; **1,500 PRs** opened (~3.5/person/day)
- Early progress was slow — not because Codex was bad, but because it **lacked tools and structure**
- The pattern they found: break large goals → small building blocks → agent assembles → compose into complex tasks
- When something went wrong: *"What is the agent still missing, and can it be supplied in an understandable, executable way?"*

---

## 🐍 Real-World Example (FastAPI + PostgreSQL + Redis)

**Task:** Add user preferences endpoints under `/api/v2/users`

| Attempt | Setup | Outcome |
|---------|-------|---------|
| Before | One sentence prompt | 40% context wasted on repo exploration; wrong patterns; runtime errors; session had to restart |
| After | `AGENTS.md` + explicit verification commands + architecture decision records | ✅ Succeeded on all 3 independent runs; ~60% better context efficiency |

**Same model. Different harness.**

---

## ✅ Key Takeaways

1. **Model capability and execution reliability are two different things** — even a thoroughbred needs good tack
2. **Check the harness first, then the model** — swapping models is the most expensive and least likely fix
3. **Every failure is a signal** — your harness has a structural defect; find it and fix it
4. **Work through the 5 layers systematically** before concluding the model isn't good enough
5. **`AGENTS.md` is the highest-ROI first step** in harness engineering
