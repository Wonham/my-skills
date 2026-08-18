"""Create a small scene used only to verify Blender CLI integration."""

import os
import sys

import bpy
from mathutils import Vector


def custom_args():
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    if len(args) != 2:
        raise SystemExit("usage: smoke_scene.py -- <render.png> <scene.blend>")
    return [os.path.abspath(path) for path in args]


def point_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


render_path, blend_path = custom_args()
os.makedirs(os.path.dirname(render_path), exist_ok=True)
os.makedirs(os.path.dirname(blend_path), exist_ok=True)

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1))
cube = bpy.context.object
cube.name = "BlenderCliSmokeCube"

material = bpy.data.materials.new("BlenderCliSmokeMaterial")
shader = material.node_tree.nodes.get("Principled BSDF")
shader.inputs["Base Color"].default_value = (0.04, 0.25, 0.8, 1.0)
shader.inputs["Metallic"].default_value = 0.2
shader.inputs["Roughness"].default_value = 0.25
cube.data.materials.append(material)

bpy.ops.mesh.primitive_plane_add(size=16)
bpy.context.object.name = "BlenderCliSmokeGround"

bpy.ops.object.light_add(type="AREA", location=(-3, -4, 6))
light = bpy.context.object
light.name = "BlenderCliSmokeLight"
light.data.energy = 1000
light.data.size = 4
point_at(light, (0, 0, 1))

bpy.ops.object.camera_add(location=(5, -7, 4))
camera = bpy.context.object
camera.name = "BlenderCliSmokeCamera"
point_at(camera, (0, 0, 1))

scene = bpy.context.scene
scene.camera = camera
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 512
scene.render.resolution_y = 512
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = render_path

bpy.ops.wm.save_as_mainfile(filepath=blend_path)
bpy.ops.render.render(write_still=True)

for output_path in (render_path, blend_path):
    if not os.path.isfile(output_path) or os.path.getsize(output_path) == 0:
        raise RuntimeError(f"Expected nonempty output: {output_path}")

print(f"RENDERED={render_path}")
print(f"SAVED={blend_path}")
