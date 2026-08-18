# Blender 5.2 CLI Notes for This Mac

Read this reference on first use, after a Blender update/reinstall, or when startup/render behavior differs.

## Verified installation

Verified on 2026-08-18:

- macOS Apple Silicon (`arm64`)
- Blender 5.2.0 LTS installed by Steam
- Real executable:

```text
/Users/wonham/Library/Application Support/Steam/steamapps/common/Blender/Blender.app/Contents/MacOS/Blender
```

`/Users/wonham/Applications/Blender.app` was a Steam launcher containing `run.sh`, not the Blender CLI binary. Always resolve again after reinstalling rather than assuming this snapshot is current.

## Stable invocation

The wrapper prepends the verified safety/error flags:

```text
--background --factory-startup --disable-autoexec --python-exit-code 1
```

For a task-local script:

```zsh
run_blender.sh --python /absolute/create_scene.py -- /absolute/render.png /absolute/scene.blend
```

For a saved scene verification pass, load the file before the Python assertion:

```zsh
run_blender.sh /absolute/scene.blend \
  --python-expr "import bpy; assert bpy.context.scene.camera is not None"
```

For direct rendering, keep the action last:

```zsh
run_blender.sh /absolute/scene.blend \
  --render-output /absolute/frame_#### \
  --render-format PNG \
  --render-frame 1
```

## Blender 5.2 API details

- Eevee engine identifier: `BLENDER_EEVEE`.
- Available engines can be queried with:

```python
scene = bpy.context.scene
engines = {
    item.identifier
    for item in scene.render.bl_rna.properties["engine"].enum_items
}
```

- New materials and the default world already have node trees. Setting `Material.use_nodes` or `World.use_nodes` emits deprecation warnings in 5.2.
- Set the active camera explicitly: `scene.camera = camera`.
- Set `scene.render.filepath` before `bpy.ops.render.render(write_still=True)`.
- Save with `bpy.ops.wm.save_as_mainfile(filepath=...)` and verify by opening the result in a second Blender process.

## Codex sandbox failure signature

Background mode inside the sandbox was reproducibly terminated with exit 139 before the Python script ran. The crash report ended in Metal backend detection around `supports_barycentric_whitelist` / `metal_is_supported`. The identical command succeeded outside the sandbox.

When this signature appears, request approval for an out-of-sandbox Blender run. Do not guess GPU flags or edit the scene script until the same minimal startup probe has been tried outside the sandbox.

## Verification checklist

- Blender process exits 0 with no traceback or deprecation warning.
- PNG or other render is nonempty and has the requested dimensions.
- `.blend` is nonempty and opens successfully in a new Blender process.
- Reopened scene contains the expected named objects, materials, lights, camera, engine, and resolution.
- Render is visually inspected when composition or appearance matters.
