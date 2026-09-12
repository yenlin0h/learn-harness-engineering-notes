# 📚 Lecture 03 Summary: Making the Repository the Single Source of Truth
---

## 🧠 Core Thesis
An AI agent has only three sources of input: system prompts/task descriptions, repository file contents, and tool execution output. 
**If knowledge isn't written into the repository, it doesn't exist for the agent.** 
The repository must become the single, authoritative "map" the agent navigates by — and how good that map is directly determines whether the agent succeeds or wanders into guesswork.

---
## 🚧 5 Questions Every Repo Must Answer (Fresh Session Test)
1. **What is this system?** — Should live in `AGENTS.md` / `README`
2. **How is it organized?** — Should live in `ARCHITECTURE.md` / module docs
3. **How do I run it?** — Should live in `Makefile` / `init.sh` / package scripts
4. **How do I verify it?** — Should live in test, lint, check commands
5. **Where are we now?** — Should live in `PROGRESS.md` / feature list / git history
Open a brand-new session, give it only the repo, and check how many it can answer. Every blank spot means the agent has to **guess** — and guessing compounds: wrong guesses become bugs, and every new session re-guesses from zero.

---
## 🛠️ The Core Principle & What To Do About It
### ✅ When the agent guesses wrong — fix the map, not the model
**Principle 1: Knowledge lives next to code**
Put a short doc in each module directory covering that module's responsibilities, interfaces, and constraints — the directory itself becomes the index.

**Principle 2: Use a standardized entry file**
`AGENTS.md` (or `CLAUDE.md`) is the agent's landing page. It should answer three things in 50–100 lines:
```markdown
- What is this project
- How do I run it
- How do I verify it
```
**Principle 3: Minimal but complete**
Every rule should earn its place — if removing it wouldn't hurt decision quality, cut it. But every fresh-session-test question must still have an answer.

**Principle 4: Update with code**
Bind doc updates to code changes. Co-locate docs with the modules they describe, and use CI to flag when docs may need a second look after a code change.

**Concrete repo structure:**
```
project/
├── AGENTS.md              # Entry: project overview, run commands, hard constraints
├── src/
│   ├── api/
│   │   ├── ARCHITECTURE.md  # API layer architecture decisions
│   │   └── ...
│   ├── db/
│   │   ├── CONSTRAINTS.md   # Database operation hard constraints
│   │   └── ...
│   └── ...
├── PROGRESS.md             # Current progress: done, in-progress, blocked
└── Makefile                # Standardized commands: setup, test, lint, check
```
> 💡 *A well-placed 50-line `ARCHITECTURE.md` next to the code is worth more than a 500-page Confluence doc nobody maintains.*
---

## ⚙️ Managing Agent State with ACID Principles
| Principle | Application |
|-----|-------|
| **Atomicity** | Commit a logical operation only once complete and verified — failed attempts are discarded whole, not partially merged |
| **Consistency** | Run verification (tests pass, zero lint errors) after each operation — never commit an inconsistent intermediate state |
| **Isolation** | Give concurrent agents separate progress files or git branches to avoid race conditions |
| **Durability** | Critical knowledge must be written into git-tracked files — what's only in session memory doesn't survive; what's not written down doesn't count |
---

## ✅ Key Takeaways
- Knowledge not in the repo doesn't exist for the agent — putting decision information into the repository is the **most fundamental harness investment**
- Use the **fresh session test** to evaluate whether your repo is a good enough map: can a new session answer all 5 basic questions?
- Good knowledge is **near the code, minimal but complete, and updated together with code** — this is a placement problem, not a "write more docs" problem
- Apply **ACID principles** to agent state management: atomic commits, consistency checks, isolation for concurrency, durability for critical knowledge
- **Knowledge decay is the biggest enemy** — outdated documentation is more dangerous than no documentation, because it confidently sends the agent in the wrong direction
