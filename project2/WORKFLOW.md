# Project 02 — Steps Followed

## Step 0 — Environment setup

```csh
source /user/caldevtools/bin/load-devtools.csh
```

Loads `node`/`npm` (and the Claude Code tooling) into the shell. Added to `~/.cshrc` so future shells pick it up automatically.

## Step 1 — Baseline setup

```csh
cd ~/harness-engineering/destination-repo/project2/starter
npm install
npm run check
```

`npm run check` just type-checks; it should pass cleanly before starting any feature work.

## Step 2 — Session A (Claude Code)

Launch Claude Code from the `starter/` directory:

```csh
claude
```

Prompt:

```text
Read AGENTS.md, docs/ARCHITECTURE.md, docs/PRODUCT.md, and feature_list.json.
Implement the "document-import" and "document-detail" features only —
do NOT implement "basic-persistence" yet. Update feature_list.json status/evidence
for the features you complete. Stop after document-import and document-detail
are working; do not start persistence.
```

Claude Code worked through:

- **Import**: renderer `ImportPanel` → preload → `ipc-handlers.ts` → `DocumentService`. Electron 32+ removed `File.path`, which had silently broken the file picker; replaced with a main-process picker via a new `SELECT_IMPORT_FILE` IPC channel backed by `dialog.showOpenDialog`.
- **Detail view**: `DocumentDetail` had a TODO where content was never loaded; wired it to a new `GET_DOCUMENT_CONTENT` IPC channel backed by the existing `DocumentService.getDocumentContent`.

Verified via `tsc -p tsconfig.node.json`, `vite build`, and direct service-level tests against temp files (the Electron binary itself wasn't installed in this sandbox, so the window couldn't be launched directly).

Before ending the session, asked Claude Code to write the handoff file:

```text
Create session-handoff.md at the project root. Summarize: what was implemented
this session (document-import, document-detail), key implementation decisions
(e.g. the Electron 32+ File.path removal workaround, the new SELECT_IMPORT_FILE
IPC channel), what remains (basic-persistence), and exact next steps for a new
agent session with no prior context.
```

Then exited (`/exit`) and committed:

```csh
cd ~/harness-engineering/destination-repo
git add -A
git commit -m "Session A: document import + detail view"
git push origin main
```

## Step 3 — Session B (fresh context, no oral handoff)

Started a brand-new Claude Code process in the same directory — exited and relaunched rather than using `/clear`, so there was no ambiguity about carried-over context:

```csh
claude
```

Gave it a deliberately thin prompt, forcing it to rely on repo state:

```text
Continue this project. Figure out what's done and what's left, then finish it.
```

Watched whether it:

- Read `session-handoff.md` and `feature_list.json` on its own
- Correctly identified `basic-persistence` as the remaining work
- Avoided re-implementing import/detail from scratch

That rediscovery time and accuracy is the actual thing being measured by this exercise, not the app itself.

## Step 4 — Compare against the reference solution

The copied repo only contains `starter/`, not `solution/`. To compare against the intended reference implementation (expanded `ARCHITECTURE.md`/`PRODUCT.md` and a complete `session-handoff.md`), see the original repo:

https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-02/solution
