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
grass_path = root + '/textures/grass.jpg'
brick_path = root + '/textures/brick.jpg'
concrete_path = root + '/textures/concrete.jpg'

# Prop paths
car_path = root + "/scenarios/Car/car.stl"
person_path = root + "/scenarios/Person/person.dae"
text_path = root + "/scenarios/Roboptics Text/text.stl"


def build():
    prev_slab = add_slab(0, (-40,-30), (90, 60), box=True)
    add_texture(prev_slab, grass_path)
    #disable dynamics faor the ground slab:
    bpy.data.objects['0_1_SLAB'].rigid_body.enabled=False;


    for i in range(0, FLOORS):
        # External columns
        c = add_column(i, (20 - WALL_THICKNESS, 12.5 - WALL_THICKNESS), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (20 - WALL_THICKNESS, -12.5 + WALL_THICKNESS), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (-20 + WALL_THICKNESS, 12.5 - WALL_THICKNESS), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (-20 + WALL_THICKNESS, -12.5 + WALL_THICKNESS), 1)
        add_texture(c, concrete_path)
        
        c = add_column(i, (15, 12.5 - WALL_THICKNESS), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (10, 12.5 - WALL_THICKNESS), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (5, 12.5 - WALL_THICKNESS), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (0, 12.5 - WALL_THICKNESS), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (-5, 12.5 - WALL_THICKNESS), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (-10, 12.5 - WALL_THICKNESS), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (-15, 12.5 - WALL_THICKNESS), 1)
        add_texture(c, concrete_path)
        
        c = add_column(i, (15, -12.5 + WALL_THICKNESS), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (10, -12.5 + WALL_THICKNESS), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (5, -12.5 + WALL_THICKNESS), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (0, -12.5 + WALL_THICKNESS), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (-5, -12.5 + WALL_THICKNESS), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (-10, -12.5 + WALL_THICKNESS), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (-15, -12.5 + WALL_THICKNESS), 1)
        add_texture(c, concrete_path)
        
        
        # Internal columns
        c = add_column(i, (-15, 6.25), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (-10, 6.25), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (-5, 6.25), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (0, 6.25), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (5, 6.25), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (10, 6.25), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (15, 6.25), 1)
        add_texture(c, concrete_path)
        
        c = add_column(i, (-15, -6.25), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (-10, -6.25), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (-5, -6.25), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (0, -6.25), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (5, -6.25), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (10, -6.25), 1)
        add_texture(c, concrete_path)
        c = add_column(i, (15, -6.25), 1)
        add_texture(c, concrete_path)
            
        # Slab
        slab = add_slab(i + 1, (-20, -12.5), (40, 25))
        add_texture(slab, concrete_path)
        
        ### RAMPS ###
        # Cuts
        bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False, location=(-12, 0, FLOORS * (WALL_HEIGHT + SLAB_THICKNESS) / 2.))
        cube = bpy.context.object
        cube.name = "Cutter"
        cube.scale=[12.5 / 2., 5 / 2., (FLOORS + 1) * (WALL_HEIGHT + SLAB_THICKNESS) / 2. - SLAB_THICKNESS]
        
        bool_diff_op(slab, cube)
        bpy.context.scene.objects.unlink(cube)
        
        # Ramps
        s = add_slab(i, (-17.5, -2.2), (12.5, 4 / 2.), rot=[0, 16, 0])
        bool_diff_op(s, slab)
        bool_diff_op(s, prev_slab)
        add_texture(s, concrete_path)
        s = add_slab(i + 1, (-18, 0.2), (13, 4 / 2.), rot=[0, -15, 0])
        bool_diff_op(s, slab)
        bool_diff_op(s, prev_slab)
        add_texture(s, concrete_path)
            
        
        ### STAIRS ###
        # Cuts
        bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False, location=(-14, 8.5, FLOORS * (WALL_HEIGHT + SLAB_THICKNESS) / 2.))
        cube = bpy.context.object
        cube.name = "Cutter"
        cube.scale=[6 / 2., 2.5 / 2., (FLOORS + 1) * (WALL_HEIGHT + SLAB_THICKNESS) / 2. - SLAB_THICKNESS]
        
        bool_diff_op(slab, cube)
        bpy.context.scene.objects.unlink(cube)
        
        # Stairs
        prev_cube = 0
        for s in range(21):
            bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False, location=((-17 + s * 0.3), 8.5, i * (SLAB_THICKNESS + WALL_HEIGHT) + (SLAB_THICKNESS + s * 0.32) / 2.))
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
    bpy.data.window_managers["WinMan"].bullet_tool.bullet_tool_neighbours=10
    bpy.data.window_managers["WinMan"].bullet_tool.bullet_tool_search_radius=20.
    bpy.data.window_managers["WinMan"].bullet_tool.bullet_tool_show_break=True
    bpy.data.window_managers["WinMan"].bullet_tool.bullet_tool_breakable=True

    # this is working with the "incorrect mass" above
    bpy.data.window_managers["WinMan"].bullet_tool.bullet_tool_break_threshold=2.5
    bpy.data.window_managers["WinMan"].bullet_tool.bullet_tool_absolut_mass=False

    # bpy.data.window_managers["WinMan"].bullet_tool.bullet_tool_break_threshold=1000.
    # bpy.data.window_managers["WinMan"].bullet_tool.bullet_tool_absolut_mass=True

    bpy.ops.bullet.update()
    

def add_props():
    # Moving Cars
    add_imported_stl(car_path,
                     (-13, -4, SLAB_THICKNESS / 2.),
                     rot=[0, 0, 0])
                     
    add_imported_stl(car_path,
                     (3, -4, SLAB_THICKNESS / 2.),
                     rot=[0, 0, 0])
                     
    add_imported_stl(car_path,
                     (-13, 4, 7 + SLAB_THICKNESS / 2.),
                     rot=[0, 0, 180])
                     
    add_imported_stl(car_path,
                     (-3, -1.25, 10.5 + SLAB_THICKNESS / 2.),
                     rot=[0, 0, 0])
                     
    add_imported_stl(car_path,
                     (13, 2, 3.5 + SLAB_THICKNESS / 2.),
                     rot=[0, 0, 0])


    # Parked Cars
    add_imported_stl(car_path,
                     (17.5, 9, 3.5 + SLAB_THICKNESS / 2.),
                     rot=[0, 0, 90])

    add_imported_stl(car_path,
                     (12.5, 9, 3.5 + SLAB_THICKNESS / 2.),
                     rot=[0, 0, 90])
                     
    add_imported_stl(car_path,
                     (2.5, 9, 3.5 + SLAB_THICKNESS / 2.),
                     rot=[0, 0, 90])
                     
    add_imported_stl(car_path,
                     (-7.5, -10, 7 + SLAB_THICKNESS / 2.),
                     rot=[0, 0, 90])
                     
    add_imported_stl(car_path,
                     (-2.5, -10, 7 + SLAB_THICKNESS / 2.),
                     rot=[0, 0, 90])
                     
    add_imported_stl(car_path,
                     (13, -9, 10.5 + SLAB_THICKNESS / 2.),
                     rot=[0, 0, 90])
                     
    add_imported_stl(car_path,
                     (17.5, -9, 10.5 + SLAB_THICKNESS / 2.),
                     rot=[0, 0, 90])

    add_imported_stl(car_path,
                     (12.5, -9, SLAB_THICKNESS / 2.),
                     rot=[0, 0, 90])
                     
    add_imported_stl(car_path,
                     (7.5, -9, SLAB_THICKNESS / 2.),
                     rot=[0, 0, 90])
                     
    add_imported_stl(car_path,
                     (2.5, -9, SLAB_THICKNESS / 2.),
                     rot=[0, 0, 90])
                     
    add_imported_stl(car_path,
                     (-7.5, -9, SLAB_THICKNESS / 2.),
                     rot=[0, 0, 90])
                     
    add_imported_stl(car_path,
                     (17.5, 9, SLAB_THICKNESS / 2.),
                     rot=[0, 0, 90])
                     
    add_imported_stl(car_path,
                     (12.5, 9, SLAB_THICKNESS / 2.),
                     rot=[0, 0, 90])
                     
    add_imported_stl(car_path,
                     (7.5, 9, SLAB_THICKNESS / 2.),
                     rot=[0, 0, 90])
                     
    add_imported_stl(car_path,
                     (2.5, 9, SLAB_THICKNESS / 2.),
                     rot=[0, 0, 90])
                     
    add_imported_stl(car_path,
                     (-2.5, 9, SLAB_THICKNESS / 2.),
                     rot=[0, 0, 90])


    # People
    add_imported_dae(person_path,
                     (-18, 8.5, SLAB_THICKNESS),
                     rot=[0, 0, -90],
                     correction=[0, 0, 0.65])

    add_imported_dae(person_path,
                     (-16.5, 10.5, 3.5 + SLAB_THICKNESS),
                     rot=[0, 0, -90],
                     correction=[0, 0, 0.65])

    add_imported_dae(person_path,
                     (-10.5, 8.5, 10.5 + SLAB_THICKNESS),
                     rot=[0, 0, 90],
                     correction=[0, 0, 0.65])

    add_imported_dae(person_path,
                     (-12.5, -2.75, SLAB_THICKNESS),
                     rot=[0, 0, 0],
                     correction=[0, 0, 0.65])

    # Roboptics
    add_imported_stl(text_path, (20, -25, SLAB_THICKNESS / 2.))



if __name__ == '__main__':
    cleanup()
    
    build()
    
    if SIMULATE:
        simulate()
        
    add_props()

