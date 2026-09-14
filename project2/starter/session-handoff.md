# Session Handoff

## What was implemented this session

Two features from `feature_list.json`, now marked `pass`:

1. **`document-import`** — Fixed a broken import flow.
2. **`document-detail`** — Implemented the missing document content viewer.

`basic-persistence` was explicitly **not** started (see below).

### document-import
- `ImportPanel` used `file.path` from an `<input type="file">` element to get a
  filesystem path to hand to the import IPC call. Electron **removed `File.path`
  in v32+**, and this project pins `electron@^33.2.0` — so `file.path` was always
  `undefined` and import silently did nothing.
- Replaced it with a main-process file picker:
  - `SELECT_IMPORT_FILE` IPC channel added to `src/shared/types.ts`.
  - Handler in `src/main/ipc-handlers.ts` calls `dialog.showOpenDialog` filtered to
    `.txt`/`.md`.
  - Exposed via preload as `window.knowledgeBase.documents.selectImportFile()`.
  - `ImportPanel` now has a "Choose File" button that calls this, then calls
    `onImport(filePath)`.
  - `App.tsx`'s `handleImport` no longer swallows errors internally — it now
    propagates so `ImportPanel` can catch and display them to the user.

### document-detail
- `DocumentDetail` had a `content` state variable that was declared but never
  populated (a `TODO` comment marked the gap).
- Added `GET_DOCUMENT_CONTENT` IPC channel, wired to the **already-existing**
  `DocumentService.getDocumentContent(id)` (no service-layer changes needed).
- Exposed via preload as `documents.getContent(id)`.
- `DocumentDetail` fetches it in a `useEffect` keyed on `document.id` and renders
  it in the existing content-viewer `<div>`.

## Key implementation decisions

- **No extra validation added.** I initially added file-size (10 MB) and extension
  validation to `DocumentService.importDocument`, matching the constraints in
  `docs/PRODUCT.md`. The user rejected that edit and asked to scope down to just
  fixing what was actually broken. Final code has **no size/extension validation**
  in the service layer — only the file dialog's extension filter constrains input.
  If this is revisited, note the user's explicit preference for minimal scope.
- **File selection moved to the main process** rather than trying to patch around
  `File.path` in the renderer (e.g. via `webUtils.getPathForFile`). This matches
  Electron's current recommended pattern and avoids renderer-side path handling
  entirely.
- **Errors now surface in the UI.** Previously `handleImport` caught and only
  `console.error`'d failures — a real failure (bad file, missing file) gave no user
  feedback. Now `ImportPanel` shows the error message inline.

## What remains: `basic-persistence`

Status in `feature_list.json` is still `not-started`. Per its description:
"Imported documents persist across app restarts via filesystem storage."

Worth checking before assuming this needs new code — `PersistenceService` and
`DocumentService` already write to `documents-meta.json` and `content/<id>.txt`
on every import/delete, which looks like real filesystem persistence already.
Investigate what's actually failing (or missing) before implementing:
- Confirm `app.getPath('userData')` resolves to a stable path across restarts
  (should be fine in packaged/dev Electron, but verify in this environment).
- Confirm documents are correctly reloaded into `DocumentList` on app relaunch
  (i.e. `App.tsx`'s initial load — check whether `refreshDocuments()` is called
  on mount at all; a quick look during this session did not confirm this).
- Check whether indexing status (`document.status`, `chunks`) also needs to
  survive restarts, or just the document list/content.

## Gotchas for a fresh agent

- **Electron binary is not installed in this sandbox** (network-restricted
  environment). `npx electron .` fails with "Electron failed to install
  correctly". You cannot visually launch the app here. Verify logic by:
  - `npx tsc -p tsconfig.node.json` for main/preload/shared/services.
  - `npx vite build` for the renderer.
  - Running compiled service code directly with `node -e "..."` against
    `dist/services/*.js` for behavioral checks (see `SESSION_SUMMARY.md` for the
    exact pattern used).
- **`npm run check` has pre-existing failures unrelated to this work.** Running
  `tsc --noEmit -p tsconfig.json` (renderer) fails with `Cannot find module
  '../../shared/types'`-style errors and unused-`React`-import errors. These
  predate this session (confirmed via `git stash` + rerunning `npm run check`
  before any edits) and are a tsconfig/module-resolution issue unrelated to
  document-import/detail. Don't assume you introduced them; don't feel obligated
  to fix them unless asked — they were out of scope here.
- **`dist/` is untracked and not gitignored.** No `.gitignore` exists in this
  project. Build artifacts were deleted after verification (`rm -rf dist`) to
  keep the working tree clean — do the same after any build-based testing.
- **`node_modules/` and `package-lock.json` are untracked** per the initial git
  status snapshot — that predates this session, not something introduced here.

## Exact next steps

1. Read `feature_list.json` entry for `basic-persistence` and re-read
   `docs/ARCHITECTURE.md`'s "Data Storage" section for the expected file layout.
2. Check `App.tsx` for whether `refreshDocuments()` (or equivalent) is called on
   initial mount via `useEffect`. If not, documents imported in a previous
   session won't show up in the list on launch even though the files are on disk
   — that's the likely actual gap, not the `PersistenceService`/`DocumentService`
   write logic (which already looks correct).
3. If the list-on-mount gap is confirmed, add a `useEffect(() => {
   refreshDocuments(); }, [])` in `App.tsx`.
4. Manually verify (or as close as this sandbox allows) that:
   - Import a doc → simulate "restart" by re-invoking `DocumentService`/`listDocuments`
     against the same data dir → confirm the doc is still listed with correct
     metadata and content.
5. Update `feature_list.json`'s `basic-persistence` entry (`status`, `evidence`,
   `testedAt`) once verified.
6. Do not touch `document-import` or `document-detail` further unless a
   regression is found — both are marked `pass` with evidence in
   `feature_list.json`.
