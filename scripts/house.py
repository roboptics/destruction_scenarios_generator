import bpy
import math
import os
import sys

root = os.environ.get('DESTRUCTION_SCENARIOS_ROOT')

if root == None:
	sys.exit(-1)

sys.path.append(root + '/scripts')
from common import *

SIMULATE = False

# Texture paths
gravel_path = root + '/textures/gravel.jpg'
brick_path = root + '/textures/brick.jpg'
concrete_path = root + '/textures/concrete.jpg'

# Prop paths
person_path = root + "/scenarios/Person/person.dae"
text_path = root + "/scenarios/Roboptics Text/text.stl"


def build():
    prev_slab = add_slab(0, (-40,-30), (90, 60), box=True)
    add_texture(prev_slab, gravel_path)
    #disable dynamics faor the ground slab:
    bpy.data.objects['0_1_SLAB'].rigid_body.enabled=False;


    for i in range(0, FLOORS):
        # Four outside walls
        s = add_wall(i, (-10.5, -6), 21, 0)
        add_texture(prev_slab, brick_path)
        if i == 0:
            add_door(s, (8, -6), i, 2)
        add_window(s, (-8, -6), i)
        add_window(s, (2, -6), i)
        add_window(s, (-2, -6), i)
        add_window(s, (8, -6), i)
        
        s = add_wall(i, (-10.5, 6), 21, 0)
        add_texture(prev_slab, brick_path)
        add_window(s, (-8, 6), i)
        add_window(s, (0, 6), i)
        add_window(s, (8, 6), i)
        
        s = add_wall(i, (-10.5, -6), 12, 90, False, False)
        add_texture(prev_slab, brick_path)
        add_window(s, (-10.5, -3), i)
        add_window(s, (-10.5, 3), i)
        
        s = add_wall(i, (10.5, 6), 12, -90, False, False)
        add_texture(prev_slab, brick_path)
        add_window(s, (10.5, -3), i)
        add_window(s, (10.5, 3), i)
        
        # Vertical inside walls
        s = add_wall(i, (-3.5, -6), 12, 90, False, False)
        add_texture(prev_slab, brick_path)
        add_door(s, (-3.5, 1.75), i, 1.5, vert=True)
        
        s = add_wall(i, (-0.5, -6), 7, 90, False, False)
        add_texture(prev_slab, brick_path)
        
        s = add_wall(i, (6, -6), 12, 90, False, False)
        add_texture(prev_slab, brick_path)
        add_door(s, (6, 1.75), i, 1.5, vert=True)
        
        # Horizontal inside walls
        s = add_wall(i, (-3.5, 0.6), 3, 0, False, False)
        add_texture(prev_slab, brick_path)
        add_door(s, (-2, 0.6), i, 1.5)
        
        s = add_wall(i, (-0.5, -1.5), 6.5, 0, False, False)
        add_texture(prev_slab, brick_path)
        add_door(s, (1.5, -1.5), i, 1.5)
        
        s = add_wall(i, (6, 0.5), 4.5, 0, False, False)
        add_texture(prev_slab, brick_path)
        add_door(s, (7.5, 0.5), i, 1.5)
            
        # Slab
        slab = add_slab(i + 1, (-10.5, -6), (21, 12))
        add_texture(slab, brick_path)
        
        if i != FLOORS - 1:
            ### STAIRS ###
            # Cuts
            bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False, location=(1.2, 4.5, FLOORS * (WALL_HEIGHT + SLAB_THICKNESS) / 2.))
            cube = bpy.context.object
            cube.name = "Cutter"
            cube.scale=[6 / 2., 2.5 / 2., (FLOORS + 1) * (WALL_HEIGHT + SLAB_THICKNESS) / 2. - SLAB_THICKNESS]
            
            bool_diff_op(slab, cube)
            bpy.context.scene.objects.unlink(cube)
            
            # Stairs
            prev_cube = 0
            for s in range(21):
                bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False, location=((4 - s * 0.3), 4.5, i * (SLAB_THICKNESS + WALL_HEIGHT) + (SLAB_THICKNESS + s * 0.32) / 2.))
                cube = bpy.context.object
                cube.scale=[0.5 / 2., 2.5 / 2., 0.2 / 2.]
                add_texture(cube, concrete_path)
                
                if s > 0:
                    bool_union_op(prev_cube, cube)
                else:
                    prev_cube = cube
            
            bool_diff_op(prev_cube, slab)
            bool_diff_op(prev_cube, prev_slab)
        
        prev_slab = slab


def simulate():
    ####
    # setup destruction physics
    ####
    # select objects to fracture
    bpy.ops.object.select_all(action="SELECT")
    for o in bpy.context.scene.objects:
        if o.type == 'MESH':
            bpy.context.scene.objects.active = o
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.subdivide()
            bpy.ops.object.mode_set(mode="OBJECT")
        
    bpy.data.objects['0_1_SLAB'].select = False
    bpy.ops.object.add_fracture_cell_objects(recursion=2,source=set(['VERT_OWN']),source_noise=1.,use_sharp_edges_apply=False,)

    # erase original objects
    bpy.ops.object.select_all(action="SELECT")
    bpy.data.objects['0_1_SLAB'].select = False
    bpy.ops.object.delete()

    # copy fractured objects from second layer to original layer
    objects_on_2nd_layer = [ob for ob in bpy.context.scene.objects if ob.layers[1]]
    for ob in objects_on_2nd_layer:
        ob.layers[0]=True;
        ob.layers[1]=False;
        
        make_rigid_body(ob)


    bpy.ops.object.select_all(action="SELECT")

    # correct mass does not give particularly good results
    # bpy.ops.rigidbody.mass_calculate(material='Brick (Soft)')

    bpy.ops.bullet.x_connect()
    bpy.ops.object.select_all(action="SELECT")
    bpy.data.window_managers["WinMan"].bullet_tool.bullet_tool_neighbours = 15
    bpy.data.window_managers["WinMan"].bullet_tool.bullet_tool_search_radius = 20.
    bpy.data.window_managers["WinMan"].bullet_tool.bullet_tool_show_break = True
    bpy.data.window_managers["WinMan"].bullet_tool.bullet_tool_breakable = True

    # this is working with the "incorrect mass" above
    bpy.data.window_managers["WinMan"].bullet_tool.bullet_tool_break_threshold = 150
    bpy.data.window_managers["WinMan"].bullet_tool.bullet_tool_absolut_mass = False

    # bpy.data.window_managers["WinMan"].bullet_tool.bullet_tool_break_threshold=1000.
    # bpy.data.window_managers["WinMan"].bullet_tool.bullet_tool_absolut_mass=True

    bpy.ops.bullet.update()


def add_props():
    # People
    for i in range(0, FLOORS):
        add_imported_dae(person_path,
                         (7.5, -3.5, i * (SLAB_THICKNESS + WALL_HEIGHT) + SLAB_THICKNESS / 2. + SLAB_THICKNESS / 2.),
                         rot=[0, 0, 0],
                         correction=[0, 0, 0.65],
                         rigid=True)

        add_imported_dae(person_path,
                         (7.5, 3.5, i * (SLAB_THICKNESS + WALL_HEIGHT) + SLAB_THICKNESS / 2. + SLAB_THICKNESS / 2.),
                         rot=[0, 0, 0],
                         correction=[0, 0, 0.65],
                         rigid=True)

        add_imported_dae(person_path,
                         (-7.5, 0, i * (SLAB_THICKNESS + WALL_HEIGHT) + SLAB_THICKNESS / 2. + SLAB_THICKNESS / 2.),
                         rot=[0, 0, 90],
                         correction=[0, 0, 0.65],
                         rigid=True)

        add_imported_dae(person_path,
                         (1.5, 0.5, i * (SLAB_THICKNESS + WALL_HEIGHT) + SLAB_THICKNESS / 2. + SLAB_THICKNESS / 2.),
                         rot=[0, 0, 0],
                         correction=[0, 0, 0.65],
                         rigid=True)

    add_imported_stl(text_path, (20, -20, SLAB_THICKNESS / 2.))



if __name__ == '__main__':
    cleanup()
    
    build()
    
    if SIMULATE:
        simulate()
        
    add_props()

