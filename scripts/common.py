import bpy
import math
import os

WALL_HEIGHT = 3.
WALL_THICKNESS = 0.4
SLAB_THICKNESS = 0.5

INDEX = 1
BOOLDIFF_ID = 1
BOOLUNION_ID = 1
FLOORS = 3


def cleanup():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    global WALL_HEIGHT, WALL_THICKNESS, SLAB_THICKNESS, INDEX, BOOLDIFF_ID, BOOLUNION_ID, FLOORS

    WALL_HEIGHT = 3.
    WALL_THICKNESS = 0.4
    SLAB_THICKNESS = 0.5

    INDEX = 1
    BOOLDIFF_ID = 1
    BOOLUNION_ID = 1
    FLOORS = 3

    

def make_rigid_body(ob):
    bpy.context.scene.objects.active = ob

    #reset object origin to center of mass (for physics to work correctly) 
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
    bpy.ops.rigidbody.object_add()
    ob.rigid_body.use_margin=True;
    ob.rigid_body.collision_margin=0.


def add_wall(stage, position, length, rot, Start=True, End=True):
    global INDEX
    
    height=stage*(SLAB_THICKNESS+WALL_HEIGHT)+SLAB_THICKNESS/2

    sz=[length+WALL_THICKNESS,WALL_THICKNESS,WALL_HEIGHT]
    lc=[length/2.,0,WALL_HEIGHT/2.]

    if not Start:
        sz[0]-=WALL_THICKNESS
        lc[0]+=WALL_THICKNESS/2.

    if not End:
        sz[0]-=WALL_THICKNESS
        lc[0]-=WALL_THICKNESS/2.

    
    bpy.ops.mesh.primitive_cube_add(location=(0,0,0),radius=1)    
    wall=bpy.context.object
    wall.name="{0}_{1}_WALL".format(stage,INDEX)
    INDEX+=1

    wall.scale=[x/2. for x in sz]
    wall.location=lc
    
    #move cursor
    saved_loc=bpy.context.scene.cursor_location.copy()
    bpy.context.scene.cursor_location=(0.,0.,0.)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.context.scene.cursor_location = saved_loc

    wall.rotation_mode = "XYZ"
    wall.rotation_euler = (0,0,math.radians(rot))
    
    #set final x,y position
    
    wall.location = [wall.location[0]+position[0], wall.location[1]+position[1], wall.location[2]+height]
    #reset object origin to center of mass (for physics to work correctly) 
    make_rigid_body(wall)
    bpy.data.objects[wall.name].rigid_body.collision_shape = 'BOX'
    
    return wall



def add_door(wall, location, stage, thickness, vert=False):
    bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False, location=(location[0], location[1], stage * (SLAB_THICKNESS + WALL_HEIGHT) + SLAB_THICKNESS / 2.))
    cube = bpy.context.object
    cube.name = "Cutter"
    if vert:
        cube.scale=[0.5 / 2., thickness / 2., WALL_HEIGHT - 0.3]
    else:
        cube.scale=[thickness / 2., 0.5 / 2., WALL_HEIGHT - 0.3]
    
    bool_diff_op(wall, cube)
    bpy.context.scene.objects.unlink(cube)
    
    
    
def add_window(wall, location, stage):
    bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False, location=(location[0], location[1], stage * (SLAB_THICKNESS + WALL_HEIGHT) + SLAB_THICKNESS / 2. + WALL_HEIGHT / 2.))
    cube = bpy.context.object
    cube.name = "Cutter"
    cube.scale=[1 / 2., 1 / 2., 1 / 2.]
    
    bool_diff_op(wall, cube)
    bpy.context.scene.objects.unlink(cube)

    
    
def add_slab(stage, position, size, rot=False, box=False):
    global INDEX
    
    height=stage*(SLAB_THICKNESS+WALL_HEIGHT)

    sz=[size[0]+WALL_THICKNESS,size[1]+WALL_THICKNESS,SLAB_THICKNESS]
    lc=[size[0]/2.,size[1]/2.,0.];

    bpy.ops.mesh.primitive_cube_add(location=(0,0,0),radius=1)    
    wall=bpy.context.object
    wall.name="{0}_{1}_SLAB".format(stage,INDEX)
    INDEX+=1

    wall.scale=[x/2. for x in sz];
    wall.location=lc;
    
    #move cursor
    saved_loc=bpy.context.scene.cursor_location.copy()
    bpy.context.scene.cursor_location=(0.,0.,0.)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.context.scene.cursor_location = saved_loc

    #set final x,y position
    wall.location = [wall.location[0]+position[0], wall.location[1]+position[1], wall.location[2]+height]
    
    # rotation
    if rot != False:
        bpy.ops.object.transform_apply()
        t_rot = (math.radians(rot[0] * -1),
                 math.radians(rot[1] * -1), 
                 math.radians(rot[2] * -1))
        
        ob = bpy.context.active_object
        ob.rotation_mode = 'ZYX'
        ob.rotation_euler = (t_rot) #set rotation to inverse
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        if rot[1] > 0:
            ob.location.x -= SLAB_THICKNESS
            ob.location.z += SLAB_THICKNESS - 0.4
        else:
            ob.location.x -= SLAB_THICKNESS + 0.1
            ob.location.z += SLAB_THICKNESS - 0.55
        
    make_rigid_body(wall)
    if box:
        bpy.data.objects[wall.name].rigid_body.collision_shape = 'BOX'
    
    return wall
    

def add_column(stage, position, thickness):
    global INDEX

    bpy.ops.mesh.primitive_cube_add(location=(position[0], position[1], stage * (WALL_HEIGHT + SLAB_THICKNESS) + SLAB_THICKNESS / 2. + WALL_HEIGHT / 2.),
                                              radius=1)
    wall=bpy.context.object
    wall.name="{0}_{1}_COL".format(stage, INDEX)
    INDEX+=1

    wall.scale=[thickness / 2., thickness / 2., WALL_HEIGHT / 2.]

    make_rigid_body(wall)
    bpy.data.objects[wall.name].rigid_body.collision_shape = 'BOX'
    
    return wall
    
    
def add_sphere(stage, location, size, mass):
    global INDEX
    
    bpy.ops.mesh.primitive_uv_sphere_add(location=(location[0], location[1], stage * (WALL_HEIGHT + SLAB_THICKNESS) + SLAB_THICKNESS / 2. + WALL_HEIGHT / 2.),
                                         size=size)

    ball=bpy.context.object
    ball.name="{0}_{1}_SPHERE".format(stage, INDEX)
    INDEX += 1
    make_rigid_body(ball)
    ball.rigid_body.mass = 100
    
    bpy.ops.object.select_pattern(pattern=ball.name)
    bpy.ops.transform.translate(value=(2, 0, 0))
    bpy.ops.anim.keyframe_insert_menu(type="Location")
    
    return ball



def bool_diff_op(obj_to_cut, obj_):
    global BOOLDIFF_ID
    
    bool_diff = obj_to_cut.modifiers.new(type="BOOLEAN", name="{0}_BOOLDIFF".format(BOOLDIFF_ID))
    bool_diff.operation = 'DIFFERENCE'
    bool_diff.object = obj_
    bpy.context.scene.objects.active = obj_to_cut
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="{0}_BOOLDIFF".format(BOOLDIFF_ID))
    
    BOOLDIFF_ID += 1


def bool_union_op(obj, obj_):
    global BOOLUNION_ID
    
    bool_union = obj.modifiers.new(type="BOOLEAN", name="{0}_BOOLUNION".format(BOOLUNION_ID))
    bool_union.operation = 'UNION'
    bool_union.object = obj_
    bpy.context.scene.objects.active = obj
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="{0}_BOOLUNION".format(BOOLUNION_ID))
    bpy.context.scene.objects.unlink(obj_)
    
    BOOLUNION_ID += 1



def add_texture(obj, path):
    texture_path = os.path.expanduser(path)
    
    try:
        img = bpy.data.images.load(texture_path)
    except:
        raise NameError("Cannot load image %s" % texture_path)
        
    # Create image texture from image
    cTex = bpy.data.textures.new('ColorTex', type = 'IMAGE')
    cTex.image = img
 
    # Create procedural texture 
    sTex = bpy.data.textures.new('BumpTex', type = 'STUCCI')
    sTex.noise_basis = 'BLENDER_ORIGINAL' 
    sTex.noise_scale = 0.25 
    sTex.noise_type = 'SOFT_NOISE' 
    sTex.saturation = 1 
    sTex.stucci_type = 'PLASTIC' 
    sTex.turbulence = 5 
 
    # Create blend texture with color ramp
    # Don't know how to add elements to ramp, so only two for now
    bTex = bpy.data.textures.new('BlendTex', type = 'BLEND')
    bTex.progression = 'SPHERICAL'
    bTex.use_color_ramp = True
    ramp = bTex.color_ramp
    values = [(0.6, (1,1,1,1)), (0.8, (0,0,0,1))]
    for n,value in enumerate(values):
        elt = ramp.elements[n]
        (pos, color) = value
        elt.position = pos
        elt.color = color
 
    # Create material
    mat = bpy.data.materials.new('TexMat')
 
    # Add texture slot for color texture
    mtex = mat.texture_slots.add()
    mtex.texture = cTex
    mtex.texture_coords = 'UV'
    mtex.use_map_color_diffuse = True 
    mtex.use_map_color_emission = True 
    mtex.emission_color_factor = 0.5
    mtex.use_map_density = True 
    mtex.mapping = 'FLAT'
    mtex.scale = [10, 10, 1]
 
    # Add texture slot for bump texture
    mtex = mat.texture_slots.add()
    mtex.texture = sTex
    mtex.texture_coords = 'ORCO'
    mtex.use_map_color_diffuse = False
    mtex.use_map_normal = True
 
    # Add texture slot 
    mtex = mat.texture_slots.add()
    mtex.texture = bTex
    mtex.texture_coords = 'UV'
    mtex.use_map_color_diffuse = True 
    mtex.diffuse_color_factor = 1.0
    mtex.blend_type = 'MULTIPLY'
 
    # Create new cube and give it UVs
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.smart_project()
    bpy.ops.object.mode_set(mode='OBJECT')
    obj = bpy.context.object
 
    # Add material to current object
    ob = bpy.context.object
    me = ob.data
    me.materials.append(mat)


def add_imported_dae(path, location, rot=False, correction=False, rigid=False):
    bpy.ops.wm.collada_import(filepath=path)
    bpy.ops.transform.translate(value=location)
    
    if rot != False:
        bpy.ops.object.transform_apply()
        t_rot = (math.radians(rot[0] * -1),
                 math.radians(rot[1] * -1), 
                 math.radians(rot[2] * -1))
        
        ob = bpy.context.active_object
        ob.rotation_mode = 'ZYX'
        ob.rotation_euler = (t_rot) #set rotation to inverse
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        if correction != False:
            ob.location.x += correction[0]
            ob.location.y += correction[1]
            ob.location.z += correction[2]

    if rigid:
        dae = bpy.context.object
        make_rigid_body(dae)
        
    
    
def add_imported_stl(path, location, rot=False, correction=False, rigid=False):
    bpy.ops.import_mesh.stl(filepath=path)
    bpy.ops.transform.translate(value=location)

    if rot != False:
        bpy.ops.object.transform_apply()
        t_rot = (math.radians(rot[0] * -1),
                 math.radians(rot[1] * -1), 
                 math.radians(rot[2] * -1))
        
        ob = bpy.context.active_object
        ob.rotation_mode = 'ZYX'
        ob.rotation_euler = (t_rot) #set rotation to inverse
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        if correction != False:
            ob.location.x += correction[0]
            ob.location.y += correction[1]
            ob.location.z += correction[2]

    if rigid:
        stl = bpy.context.object
        make_rigid_body(stl)



def add_roboptics_text(location):
    bpy.ops.object.text_add()
    ob = bpy.context.object
    ob.data.body = "Destruction scenario provided uRoboptics."
    ob.location.x += location[0]
    ob.location.y += location[1]
    ob.location.z += location[2]
    
