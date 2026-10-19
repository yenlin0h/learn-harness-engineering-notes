# 📚 Lecture 06 Summary: Make the Agent Initialize Before Every Work Session
---
## 🧠 Core Thesis
Initialization and implementation are two fundamentally different kinds of work, and mixing them in one session drags both down. When an agent starts feature work immediately, it spends much of the session figuring out how the project works (test setup, migration formats, structure) instead of building the feature.
**Treat initialization as its own phase, and make its output infrastructure, not business code.** Get the environment running, verify the tests, and record how the project works before any feature is written.

---
## 🚧 The Mixed-Session Trap
### Why it happens
- **Implementation** aims to maximize the quantity and quality of verified features.
- **Initialization** aims to maximize the reliability and efficiency of all later implementation.
When both are combined, the agent faces a multi-objective problem with no explicit priorities. It gravitates toward feature code because that is the visible output. It neglects infrastructure because that value only shows up in later sessions.
### What goes wrong
- **Weak infrastructure:** Tests are configured but never verified, lint rules are too loose, and no progress file exists. The next session doesn't know how to run, test, or continue the project.
- **Unverified accumulation:** Code written before the test framework works may have a flawed design. The more code written up front, the more has to be torn down later.
- **Wasted context budget:** Setup consumes budget, so fewer features get finished, and the setup is still poor. This is the worst of both worlds.
- **Implicit assumption landmines:** Unrecorded decisions get contradicted later. For example, session 1 picks Vitest and session 2 introduces Jest, so two test frameworks coexist.
---
## 🛠️ Core Concepts
- **Initialization phase:** The first phase of the agent lifecycle. It only establishes prerequisites and involves no feature development.
- **Startup readiness checklist:** Four required conditions for a fresh session to operate the project: can **start**, can **test**, can **see progress**, can **pick up next steps**.
- **Scratch vs. template:** Starting from an empty directory forces the agent to infer structure. Starting from a template means infrastructure is already in place, and this far outperforms starting from scratch.
- **Always ready to hand off:** A fresh agent can take over just by reading the repo, with no verbal explanation.
- **Time to first passing test:** The time from project start until the first feature passes verification. This is the core metric of initialization efficiency.
- **Subsequent-session success rate:** The share of later sessions that succeed without implicit knowledge. This is the best measure of initialization quality.
---
## ✂️ How to Do Initialization Right
### Session 1 does only initialization and produces:
1. **Runnable environment:** The project starts, dependencies are installed, and there are no environment issues.
2. **Verifiable test framework:** At least one example test passes.
3. **Startup readiness checklist document:** Tells later sessions how to start, test, and navigate the project.
4. **Task breakdown:** An ordered task list where each task has clear acceptance criteria.
5. **Git commit as checkpoint:** A clean commit that all later work starts from.
Example readiness checklist:
```markdown
# Startup Readiness Checklist
## Start Commands
- Install dependencies: `make setup`
- Start dev server: `make dev`
- Run tests: `make test`
- Full verification: `make check`
## Current State
- Test framework configured (Vitest + React Testing Library)
- Example test passing (1/1)
- Lint rules configured (ESLint + Prettier)
## Project Structure
- src/ — Source code
- tests/ — Test files
```
### Start from a template
Use create-react-app, fastapi-template, or similar to preset the directory structure, dependencies, and test framework. This leaves only project-specific setup to do.
### Initialization Acceptance Checklist
- [ ] `make setup` succeeds from scratch
- [ ] `make test` has at least one passing test
- [ ] A new session can answer "how to run" and "how to test" from the repo alone
- [ ] A task breakdown file exists with at least 3 tasks
- [ ] Everything is committed to git
Completion is judged by these conditions, **not** by how much code was written.
---
## 🔬 Illustrative Example (React Project)
> Assumed scenario for teaching, not a published experiment.
| | Mixed approach | Dedicated initialization |
|---|---|---|
| **Session 1** | Scaffolding and first feature together | Template, Vitest + RTL, one verified test, checklist, task list, commit |
| **Repo state** | No documented commands, progress file, or task list | Fully documented and ready to hand off |
| **Session 2 startup** | ~20 min inferring structure, tests, and build | Under 3 min, starts directly from the task list |
| **Whole project** | ~60% more total rebuild time | Baseline |
The extra time spent on initialization was recovered many times over in later sessions.
---
## ✅ Key Takeaways
- **Different goals, different phases.** Mixing initialization and implementation drags both down.
- **Initialization outputs infrastructure, not business code.** That means a runnable environment, verifiable tests, a readiness checklist, and a task breakdown.
- **Validate with four conditions.** The project must be able to start, test, show progress, and let a fresh session pick up next steps.
- **Templates beat scratch.** Use them to preset standardized infrastructure.
- **Record every decision.** Unrecorded choices, like the test framework, lead to contradictory choices later.
- **Initialization is an upfront investment, not extra cost.** The time is typically recovered within the next 3–4 sessions.
---
## Challenges to the Argument
### 1. The evidence is assumed, not observed
The lecture says twice that its scenarios are "assumed for explanation." Even so, it states "~60% more rebuild time" and "recovered within 3–4 sessions" as if they were findings.
- Where would those numbers come from in practice?
- Would they hold for a two-session project? Or for a 50-session one?
### 2. "Initialization vs. implementation" is a false binary
Real projects don't have one clean setup moment. Dependencies change, a new service gets added, and a test strategy turns out wrong. The lecture treats initialization as a one-time Session 1 event, but it's closer to an ongoing maintenance activity.
### 3. It's mostly about greenfield projects
Most Siemens-style work is brownfield, with existing code, legacy build systems, and CI pipelines nobody fully understands. For those, "don't write any feature code in session 1" is much harder.
- Initialization becomes discovery and documentation of an existing system, which is a different task.
### 4. The "multi-objective optimization" argument is hand-wavy
The claim is that the agent gravitates to feature code because it's visible output. You can fix this by prompting for priorities and acceptance criteria, which is cheaper than a separate phase.
- The lecture doesn't show that separation beats good instructions inside a single session.
### 5. The "worst of both worlds" claim is overstated
Sometimes the quickest way to learn what infrastructure you need is to build a thin vertical slice. A strict ban on feature code can produce speculative infrastructure, such as a test setup that doesn't fit the real needs.
- Unverified early design decisions are a risk in initialization too.
### 6. A task breakdown made before any implementation may be wrong
Writing an ordered list of tasks with acceptance criteria up front assumes you already understand the problem. The breakdown will probably change after Task 1, so it needs a revision process, which the lecture doesn't mention.
- Otherwise the stale plan becomes the same kind of "instruction debt" that Lecture 04 warned about.
