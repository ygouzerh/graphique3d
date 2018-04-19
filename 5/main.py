#!/usr/bin/env python3
"""
Python OpenGL - Hierarchical modeling
"""
# Python built-in modules
import os                           # os function, i.e. checking file status

# External, non built-in modules
import glfw                         # lean window system wrapper for OpenGL
import numpy as np
import OpenGL.GL as GL              # standard Python OpenGL wrapper
from PIL import Image               # load images for textures
from itertools import cycle
from opengl_tools.viewer import Viewer
from opengl_tools.shader import Shader
from opengl_tools.loader import load
from opengl_tools.transform import identity, translate, rotate, \
                                    scale, vec, lerp, \
                                    quaternion_slerp, quaternion_matrix, quaternion, \
                                    quaternion_from_euler
from bisect import bisect_left
from opengl_tools.color_mesh import ColorMesh
from opengl_tools.node import Node, RotationControlNode
from opengl_tools.vertex_array import VertexArray
import pyassimp

class Cylinder(Node):
    """ Very simple cylinder based on practical 2 load function """
    def __init__(self):
        super().__init__()
        self.add(*load('cylinder.obj'))  # just load the cylinder from file

class Suzanne(Node):
    """ Suzanne node """
    def __init__(self, light_vector):
        super().__init__()
        # Get the only ione suzanne color mesh
        objects = load("suzanne.obj")
        assert len(objects)
        self.color_mesh = objects[0]
        # Add the light
        self.color_mesh.addUniform3fv({"light" :light_vector})
        print(self.color_mesh)
        self.add(self.color_mesh)

class KeyFrameControlNode(Node):
    """ Place node with transform keys above a controlled subtree """
    def __init__(self, translate_keys, rotate_keys, scale_keys, **kwargs):
        # TODO : Verify
        super().__init__()
        self.keyframes = TransformKeyFrames(translate_keys, rotate_keys, scale_keys)

    def draw(self, projection, view, model, color_shader, **param):
        """ When redraw requested, interpolate our node transform from keys """
        self.transform = self.keyframes.value(glfw.get_time())
        super().draw(projection, view, model, color_shader, **param)

class TransformKeyFrames:
    """ KeyFrames-like object dedicated to 3D transforms """
    def __init__(self, translate_keys, rotate_keys, scale_keys):
        """ stores 3 keyframe sets for translation, rotation, scale """
        self.translate_keyframes = KeyFrames(translate_keys)
        self.rotate_keyframes = KeyFrames(rotate_keys, quaternion_slerp)
        self.scale_keyframes = KeyFrames(scale_keys)

    def value(self, time):
        """ Compute each component's interpolation and compose TRS matrix """
        translate_value = translate(self.translate_keyframes.value(time))
        rotate_value = quaternion_matrix(self.rotate_keyframes.value(time))
        scale_value = scale(self.rotate_keyframes.value(time))
        return scale_value@rotate_value@translate_value

class KeyFrames:
    """ Stores keyframe pairs for any value type with interpolation_function"""
    def __init__(self, time_value_pairs, interpolation_function=lerp):
        if isinstance(time_value_pairs, dict):  # convert to list of pairs
            time_value_pairs = time_value_pairs.items()
        keyframes = sorted(((key[0], key[1]) for key in time_value_pairs))
        self.times, self.values = zip(*keyframes)  # pairs list -> 2 lists
        self.interpolate = interpolation_function

    def value(self, time):
        """ Computes interpolated value from keyframes, for a given time """
        # 1. ensure time is within bounds else return boundary keyframe
        minBound = self.times[0]
        maxBound = self.times[-1]
        if(time <= minBound):
            return self.values[self.times.index(minBound)]
        elif (time >= maxBound):
            return self.values[self.times.index(maxBound)]
        # 2. search for closest index entry in self.times, using bisect_left function
        indexInsertion = bisect_left(self.times, time)
        # 3. using the retrieved index, interpolate between the two neighboring values
        # in self.values, using the initially stored self.interpolate function
        fraction = (time-self.times[indexInsertion-1])/\
                    (self.times[indexInsertion]-self.times[indexInsertion-1])
        return self.interpolate(self.values[indexInsertion-1], self.values[indexInsertion],fraction)

class ViewerAnimation(Viewer):
    """ Viewer for the robotic arm project """
    def do_for_each_drawable(self, drawable, view, projection, model, **param):
        drawable.draw(projection, view, model, self.shaders, color=(1, 0, 1), win=self.win, **param)
        if glfw.get_key(self.win, glfw.KEY_F2) == glfw.PRESS:
            glfw.set_time(0)

def test_key_frames_1d():
    """ Test KeyFrames 1D"""
    my_keyframes = KeyFrames({0: 1, 3: 7, 6: 20})
    assert(my_keyframes.value(0) == 1)
    assert(my_keyframes.value(1.5) == 4)
    assert(my_keyframes.value(6) == 20)
    print("Test KeyFrames 1D : OK")

def test_key_frames_vec():
    """ Test KeyFrames vec"""
    vector_keyframes = KeyFrames({0: vec(1, 0, 0), 3: vec(0, 1, 0), 6: vec(0, 0, 1)})
    my_keyframes = KeyFrames({0: 1, 3: 7, 6: 20})
    # should display numpy vector (0.5, 0.5, 0)
    print("Test KeyFrames vec for 1.5 : ", end="")
    print(vector_keyframes.value(1.5))

def test_transformation():
    """ test transformation """
    translate_keys = {0: vec(0, 0, 0), 2: vec(1, 1, 0), 4: vec(0, 0, 0)}
    rotate_keys = {0: quaternion(), 2: quaternion_from_euler(180, 45, 90),
                   3: quaternion_from_euler(180, 0, 180), 4: quaternion()}
    scale_keys = {0: 1, 2: 0.5, 4: 1}
    keyframes = TransformKeyFrames(translate_keys, rotate_keys, scale_keys)
    print("Test for transformation keyframes : ", end="")
    print(keyframes.value(1.5))

def launch_windows():
    """ create a window, add scene objects, then run rendering loop """
    glfw.init()
    shaders_repertory = "../shaders/"
    vert_name = "lambert_vert.glsl"
    frag_name = "lambert_frag.glsl"
    viewer = ViewerAnimation(shaders_repertory+vert_name, shaders_repertory+frag_name)
    translate_keys = {0: vec(0, 0, 0), 2: vec(1, 1, 0), 4: vec(0, 0, 0)}
    rotate_keys = {0: quaternion(), 2: quaternion_from_euler(180, 45, 90),
                   3: quaternion_from_euler(180, 0, 180), 4: quaternion()}
    scale_keys = {0: 1, 2: 0.5, 4: 1}
    keynode = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
    keynode.add(Cylinder())
    viewer.add(keynode)
    viewer.run()
    glfw.terminate()           # destroy all glfw windows and GL contexts
# -------------- main program and scene setup --------------------------------
def main():
    """ Main Loop """
    test_key_frames_1d()
    test_key_frames_vec()
    test_transformation()
    launch_windows()

if __name__ == '__main__':

    main()                     # main function keeps variables locally scoped
