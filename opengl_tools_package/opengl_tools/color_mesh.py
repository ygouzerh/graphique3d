#!/usr/bin/env python3
"""
ColorMesh, high level object for an object
"""

from opengl_tools.vertex_array import VertexArray
import OpenGL.GL as GL              # standard Python OpenGL wrapper

class ColorMesh:
    """ ColorMesh, high level object for an object """

    def __init__(self, attributes, index=None, uniforms={}, primitive=GL.GL_TRIANGLES, usage=GL.GL_STATIC_DRAW):

        self.attributes = attributes
        self.index = index
        self.primitive=primitive
        self.usage = usage
        self.uniforms=uniforms
        self.vertex_array = VertexArray(self.attributes, self.index, self.usage)

    def draw(self, projection, view, model, color_shader, color=(1, 1, 1, 1), **param):
        """
            Draw the vertex and pass differents parameters to the shader
        """
        GL.glUseProgram(color_shader.glid)

        projection_location = GL.glGetUniformLocation(color_shader.glid, 'projection')
        view_location = GL.glGetUniformLocation(color_shader.glid, 'view')
        model_location = GL.glGetUniformLocation(color_shader.glid, 'model')
        color_location = GL.glGetUniformLocation(color_shader.glid, 'color')

        GL.glUniformMatrix4fv(projection_location, 1, True, projection)
        GL.glUniformMatrix4fv(view_location, 1, True, view)
        GL.glUniformMatrix4fv(model_location, 1, True, model)
        GL.glUniform3fv(color_location, 1, color)

        # Add the uniforms parameters
        for key, value in self.uniforms.items():
            location = GL.glGetUniformLocation(color_shader.glid, key)
            GL.glUniformMatrix4fv(location, 1, True, value)

        # Add the other parameters
        for key, value in param.items():
            location = GL.glGetUniformLocation(color_shader.glid, key)
            GL.glUniformMatrix4fv(location, 1, True, value)

        # Call the shader
        self.vertex_array.draw(self.primitive)

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

    def addUniform(self, uniform):
        """ Add a tuple of uniforms variables """
        for key, value in uniform.items():
            self.uniforms[key] = value

    def __str__(self):
        start = "ColorMesh("
        attributes = "Attributes : \n"
        for index, value in enumerate(self.attributes):
            attributes += "\nattribut {}: \n {}".format(index, value)
        usage = "usage : {} ".format(self.usage)
        primitive = "primitive : {}".format(self.primitive)
        end = ")\n"
        object_str = "{} {}\n{} , {} {}".format(start, attributes,
                                                usage, primitive, end)
        return object_str

    def __del__(self):
        del(self.vertex_array)
