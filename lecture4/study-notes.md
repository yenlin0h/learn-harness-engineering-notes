# 📚 Lecture 04 Summary: Split Instructions Across Files
---

## 🧠 Core Thesis
A giant `AGENTS.md` file eventually becomes a liability rather than an advantage. When every rule, historical note, coding preference, and deployment instruction is placed in one document, the agent must process large amounts of irrelevant information. Critical constraints become harder to recall, contradictions accumulate, and less context remains for understanding the actual task.

**The entry instruction file should be a short, high-priority router—not an encyclopedia.** Keep essential guidance close at hand and move specialized information into topic documents that are revealed only when relevant.

---

## 🚧 The Giant Instruction File Trap

### The vicious cycle
1. The agent makes a mistake.
2. A new rule is added to `AGENTS.md` to prevent it.
3. Another mistake occurs, so another rule is added.
4. The file grows until its size reduces agent performance.

Adding rules feels like a quick fix, but without regular pruning it creates instruction debt.

### What goes wrong
- **Context budget is consumed:** A 600-line file can use 10,000–20,000 tokens that would otherwise support code reading, tool output, and reasoning.
- **Critical rules get lost in the middle:** LLMs recall information at the beginning and end of long texts more reliably than information in the middle. A security rule buried at line 300 is easy to miss.
- **Priority becomes unclear:** Hard constraints, design preferences, and historical lessons appear identical, even though they have very different importance.
- **Maintenance decays:** Outdated rules are rarely removed, so the file grows and its signal-to-noise ratio declines.
- **Contradictions accumulate:** Rules added at different times may conflict, leaving the agent to choose inconsistently.

---

## 🛠️ Core Concepts

- **Instruction bloat:** When instructions occupy roughly 10–15% of the context window, they begin crowding out task-specific reasoning.
- **Lost in the middle:** Information in the center of long documents is less likely to be used effectively than information at the beginning or end.
- **Instruction signal-to-noise ratio:** The proportion of instructions relevant to the current task. Splitting documents increases this ratio.
- **Entry file:** A short file that provides essential guidance and routes the agent to more detailed documentation.
- **Reveal on demand:** Provide the overview first and load detailed instructions only when the task requires them.
- **Priority signaling:** Clearly separate non-negotiable constraints from recommendations and historical context.

---

## ✂️ How to Split Instructions

### Keep in `AGENTS.md` — ideally 50–200 lines
Include only:

1. **Project overview:** One or two sentences describing the system and technology stack.
2. **Quick-start commands:** Setup, test, and full verification commands.
3. **Global hard constraints:** No more than approximately 15 non-negotiable rules.
4. **Topic-document links:** A one-line description and the condition under which each document applies.

Example structure:

```markdown
# AGENTS.md

## Project Overview
Python 3.11 FastAPI backend, PostgreSQL 15 database.

## Quick Start
- Install: `make setup`
- Test: `make test`
- Full verification: `make check`

## Hard Constraints
- All APIs must use OAuth 2.0 authentication
- All database queries must use SQLAlchemy 2.0 syntax
- All PRs must pass pytest + mypy --strict + ruff check

## Topic Docs
- API Design Patterns (`docs/api-patterns.md`) — Required when adding endpoints
- Database Rules (`docs/database-rules.md`) — Required when modifying database operations
- Testing Standards (`docs/testing-standards.md`) — Reference when writing tests
```

### Put in topic documents — typically 50–150 lines
Create focused documents such as:

- `docs/api-patterns.md`
- `docs/database-rules.md`
- `docs/testing-standards.md`
- `docs/deployment.md`

Organize them by subject and load them only when relevant.

### Put guidance in the code when possible
Type definitions, interface comments, configuration explanations, and other code-specific knowledge are often best placed directly beside the code. The agent naturally encounters this information while inspecting the relevant implementation, avoiding duplicate instructions.

---

## 🧭 Instruction Lifecycle Management
Every instruction should record:

- **Source:** Why was this rule added?
- **Applicability:** When does it apply?
- **Expiry condition:** When can it be removed?

Audit instruction files regularly. Delete rules that are outdated, redundant, or contradictory. Treat instructions like code dependencies: unused dependencies slow the system down and should be removed.

If an instruction must remain in the entry file, put it at the **top or bottom**, not in the middle. However, routing it to a focused topic document is usually the better solution.

---

## ✅ Key Takeaways

- **“Add a rule” is short-term pain relief and long-term poison.** Before adding a rule, decide whether it belongs in a focused topic document.
- **`AGENTS.md` is a router, not an encyclopedia.** Keep it to roughly 50–200 lines with overview information, hard constraints, and links.
- **Use reveal-on-demand documentation.** Load API, database, testing, and deployment guidance only when the task needs it.
- **Protect critical constraints.** Put them at the top or bottom of the entry file, or route them to a clearly relevant document.
- **Manage instruction bloat like technical debt.** Audit regularly and remove outdated, duplicate, or contradictory guidance.
- **Improve signal-to-noise ratio.** The agent should spend its context budget on understanding, changing, and verifying the code—not on irrelevant instructions.

---
