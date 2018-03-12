#!/usr/bin/env python3
"""
ColorMesh, high level object for an object
"""

from opengl_tools.vertex_array import VertexArray
import OpenGL.GL as GL              # standard Python OpenGL wrapper

class ColorMesh:
    """ ColorMesh, high level object for an object """

    def __init__(self, attributes, index=None):

        self.attributes = attributes
        self.index = index

        self.vertex_array = VertexArray(self.attributes, self.index)

    def draw(self, projection, view, model, color_shader, color=(1, 1, 1, 1), **param):

        GL.glUseProgram(color_shader.glid)

        projection_location = GL.glGetUniformLocation(color_shader.glid, 'projection')
        view_location = GL.glGetUniformLocation(color_shader.glid, 'view')
        model_location = GL.glGetUniformLocation(color_shader.glid, 'model')
        color_location = GL.glGetUniformLocation(color_shader.glid, 'color')

        GL.glUniformMatrix4fv(projection_location, 1, True, projection)
        GL.glUniformMatrix4fv(view_location, 1, True, view)
        GL.glUniformMatrix4fv(model_location, 1, True, model)
        GL.glUniform3fv(color_location, 1, color)

        self.vertex_array.draw()

    def updateVertexArray(self):
        self.vertex_array = VertexArray(self.attributes, self.index)

    def getAttributes(self):
        return self.attributes

    def getIndex(self):
        return self.index;

    def setAttributes(self, attributes):
        if attributes is not None:
            self.attributes = attributes
            self.updateVertexArray()
        else :
            raise ValueError("Attributes parameter need to be different from None")

    def setIndex(self, index):
        self.index = index
        self.updateVertexArray()

    def addAttribut(self, attribut):
        if attribut is not None:
            self.setAttributes(self.getAttributes() + [attribut])
        else:
            raise ValueError("Attribut parameter need to be different from None")

    def __del__(self):
        del(self.vertex_array)
