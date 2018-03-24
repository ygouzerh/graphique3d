#!/usr/bin/env python3
"""
Create Node to hierachical modeling
"""
import glfw                         # lean window system wrapper for OpenGL
from opengl_tools.transform import identity
from opengl_tools.axis import xAxis, yAxis, zAxis
from opengl_tools.transform import rotate

class Node:
    """ Scene graph transform and parameter broadcast node """
    def __init__(self, name='', children=(), transform=identity(), **param):
        self.transform, self.param, self.name = transform, param, name
        self.children = list(iter(children))
        # For each node, we will have his axis
        self.add(xAxis(), yAxis(), zAxis())

    def add(self, *drawables):
        """ Add drawables to this node, simply updating children list """
        self.children.extend(drawables)

    def draw(self, projection, view, model, color_shader, **param):
        """ Recursive draw, passing down named parameters & model matrix. """
        # merge named parameters given at initialization with those given here
        param = dict(param, **self.param)
        model = model @ self.transform
        # Draw the Axis with their right color
        for child in self.children:
            child.draw(projection, view, model, color_shader, **param)

class RotationControlNode(Node):
    def __init__(self, key_up, key_down, axis, angle=0, **param):
        super().__init__(**param)   # forward base constructor named arguments
        self.angle, self.axis = angle, axis
        self.key_up, self.key_down = key_up, key_down

    def draw(self, projection, view, model, color_shader, win=None, **param):
        assert win is not None
        self.angle += 2 * int(glfw.get_key(win, self.key_up) == glfw.PRESS)
        self.angle -= 2 * int(glfw.get_key(win, self.key_down) == glfw.PRESS)
        self.transform = rotate(axis=self.axis, angle=self.angle)

        # call Node's draw method to pursue the hierarchical tree calling
        super().draw(projection, view, model, color_shader, win=win, **param)
