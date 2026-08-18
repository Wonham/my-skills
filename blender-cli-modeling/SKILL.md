---
name: blender-cli-modeling
description: Use when creating, editing, rendering, exporting, or verifying Blender scenes through Blender CLI or bpy, especially headless modeling on macOS.
---

# Blender CLI Modeling

Use Blender's bundled Python through the CLI. Prefer a task-local `bpy` script and reviewable outputs over a persistent add-on, daemon, or WebSocket server.

## Workflow

1. Inspect the requested inputs and choose explicit output paths. Preserve source `.blend` and asset files unless replacement was requested.
2. Write the smallest task-local Python script that builds or edits the scene. Parse custom arguments only after `--`.
3. Run `scripts/run_blender.sh` with the Blender arguments. In Codex on this Mac, request sandbox escalation for the wrapper: background startup inside the sandbox was verified to crash during Metal detection with exit 139.
4. Treat any nonzero exit as failure. The wrapper supplies `--python-exit-code 1`, so Python exceptions propagate correctly.
5. Verify the artifact, not just console text: require nonempty output, reopen saved `.blend` in a fresh Blender process, assert important scene state, inspect image dimensions, and visually review rendered images.

```zsh
SKILL_DIR="$HOME/.codex/skills/blender-cli-modeling"
"$SKILL_DIR/scripts/run_blender.sh" \
  --python /absolute/path/create_scene.py -- \
  /absolute/path/render.png /absolute/path/scene.blend
```

Use `scripts/smoke_scene.py` only to diagnose a new installation or changed Blender version. User scenes should get task-specific scripts.

## Invariants

- Blender arguments execute in order. Load a `.blend` before overrides; put `--render-frame` or `--render-anim` last.
- Use absolute paths because workspace names may contain spaces or non-ASCII characters.
- Do not run `bpy` with system Python; run it through Blender.
- Do not add third-party Python packages unless the task requires them and the user authorizes installation.
- Do not claim success from a generated file alone; reopen or parse it and inspect the render when visual quality matters.

For this machine's verified Blender 5.2 behavior, engine identifiers, invocation pattern, and failure signatures, read [references/blender-5.2-macos.md](references/blender-5.2-macos.md).

## Common mistakes

| Symptom | Correction |
|---|---|
| `Contents/MacOS/Blender` missing under `~/Applications` | That app may be a Steam URL launcher; use the real Steam library executable resolved by the wrapper. |
| Exit 139 before Python runs | Re-run outside the Codex sandbox with approval; do not change scene code first. |
| Python traceback but command appears successful | Use `--python-exit-code 1` (already supplied by the wrapper). |
| Eevee enum rejected | On verified Blender 5.2 use `BLENDER_EEVEE`; query `scene.render.bl_rna.properties["engine"]` for portability. |
| Render exists but is wrong | Check camera assignment, lighting, resolution, output format, then view the image. |
