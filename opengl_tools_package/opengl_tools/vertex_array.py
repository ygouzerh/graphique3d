#!/usr/bin/env python3
#!/usr/bin/env python3
"""
Low Level OpenGL Wrapper for VertexArray
"""

import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np
from opengl_tools.transform import translate, rotate, scale, vec, frustum, perspective

class VertexArray:
    def __init__(self, attributes, index=None, usage=GL.GL_STATIC_DRAW):

        self.index = index
        self.glid = GL.glGenVertexArrays(1)            # create a vertex array OpenGL identifier
        GL.glBindVertexArray(self.glid)                # make it active for receiving state below
        self.buffers = []

        for number, data in enumerate(attributes):
            self.buffers += [GL.glGenBuffers(1)]            # create one OpenGL buffer for our position attribute
            GL.glEnableVertexAttribArray(number)           # assign state below to shader attribute layout = 0
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[number])                    # our created position buffer
            GL.glBufferData(GL.GL_ARRAY_BUFFER, data, usage)   # upload our vertex data to it
            GL.glVertexAttribPointer(number, 3, GL.GL_FLOAT, False, 0, None)        # describe array unit as 2 floats

        if index is not None:
            self.buffers += [GL.glGenBuffers(1)]                                           # create GPU index buffer
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.buffers[-1])                  # make it active to receive
            GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.index, usage)     # our index array here

        # when drawing in the rendering loop: use glDrawArray for vertex arrays
        # cleanup and unbind so no accidental subsequent state update
        GL.glBindVertexArray(0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

    def draw(self, primitive=GL.GL_TRIANGLES):
        GL.glBindVertexArray(self.glid)                                         # activate our vertex array

        if self.index is not None:
            GL.glDrawElements(primitive, self.index.size, GL.GL_UNSIGNED_INT, None)  # 9 indexed verts = 3 triangles
        else :
            GL.glDrawArrays(primitive, 0, 3)

        GL.glBindVertexArray(0)

    def __del__(self):
        GL.glDeleteVertexArrays(1, [self.glid])
        # We get the len with len(self.buffers), because the size could change
        GL.glDeleteBuffers(len(self.buffers), self.buffers)
