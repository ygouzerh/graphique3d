#!/usr/bin/env python3
"""
Pyramid as scene object
"""
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np                  # all matrix manipulations & OpenGL args
from color_mesh import ColorMesh

class PyramidMultiColors:
    """Pyramid wih multiple colors"""

    def __init__(self):
        # one time initialization
        self.position = np.array(((0, 1, 0), (-0.5, 0, 0.5), (0.5, 0, 0.5), (0.5, 0, -0.5), (-0.5, 0, -0.5)), np.float32)
        self.index = np.array((0, 1, 2, 0, 2, 3, 0, 3, 4, 0, 4, 1), np.uint32)
        color = np.array(((1, 0, 0), (0, 0, 1), (0, 1, 0),(1, 1, 0), (0, 1, 1)), 'f')

        self.glid = GL.glGenVertexArrays(1)            # create a vertex array OpenGL identifier
        GL.glBindVertexArray(self.glid)                # make it active for receiving state below

        self.buffers = [GL.glGenBuffers(1)]            # create one OpenGL buffer for our position attribute
        GL.glEnableVertexAttribArray(0)           # assign state below to shader attribute layout = 0
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[0])                    # our created position buffer
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.position, GL.GL_STATIC_DRAW)   # upload our vertex data to it
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, 0, None)        # describe array unit as 2 floats

        self.buffers += [GL.glGenBuffers(1)]                                           # create GPU index buffer
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.buffers[-1])                  # make it active to receive
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.index, GL.GL_STATIC_DRAW)     # our index array here

        self.buffers += [GL.glGenBuffers(1)]                                           # create GPU index buffer
        GL.glEnableVertexAttribArray(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[-1])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, color, GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, False, 0, None)        # describe array unit as 2 floats

        # when drawing in the rendering loop: use glDrawArray for vertex arrays
        # cleanup and unbind so no accidental subsequent state update
        GL.glBindVertexArray(0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

    def draw(self, projection, view, model, color_shader, color, scaler, rotater):
        GL.glUseProgram(color_shader.glid)
        my_color_location = GL.glGetUniformLocation(color_shader.glid, 'color')
        # hard coded color : (0.6, 0.6, 0.9)
        GL.glUniform3fv(my_color_location, 1, (0.6, 0.6, 0.9))

        matrix_location = GL.glGetUniformLocation(color_shader.glid, 'matrix')
        GL.glUniformMatrix4fv(matrix_location, 1, True,
                                perspective(35, 640/480, 0.001, 100)@translate(0,0,-1)@rotate(vec(0, 1, 0), rotater)@scale(scaler))
        GL.glBindVertexArray(self.glid)                                         # activate our vertex array
        GL.glDrawElements(GL.GL_TRIANGLES, self.index.size, GL.GL_UNSIGNED_INT, None)  # 9 indexed verts = 3 triangles

    def __del__(self):
        GL.glDeleteVertexArrays(1, [self.glid])
        GL.glDeleteBuffers(1, self.buffers)

class Pyramid(ColorMesh):

    def __init__(self, position=None, index=None):
        if position is None:
            self.position = np.array(((0, 1, 0), (-0.5, 0, 0.5), (0.5, 0, 0.5), (0.5, 0, -0.5), (-0.5, 0, -0.5)), np.float32)
        else :
            self.position = position

        if index is None:
            self.index = index = np.array((0, 1, 2, 0, 2, 3, 0, 3, 4, 0, 4, 1), np.uint32)
        else:
            self.index = index

        super().__init__([self.position], self.index)

class PyramidColored(Pyramid):

    def __init__(self, color=None, position=None, index=None):
        super().__init__(position, index)
        if color is None:
            self.color = np.array(((1, 0, 0), (0, 0, 1), (0, 1, 0),(1, 1, 0), (0, 1, 1)), 'f')
        else :
            self.color = color
        super().addAttribut(self.color)
