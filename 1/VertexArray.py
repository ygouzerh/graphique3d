#!/usr/bin/env python3
"""
VertexArray Wrapper
"""

import OpenGL.GL as GL              # standard Python OpenGL wrapper
from transform import translate, rotate, scale, vec, frustum, perspective

class VertexArray:
    def __init__(self, attributes, index=None):

        self.index = index
        size = len(attributes)
        self.buffers = []
        if size > 1:
            self.buffers = GL.glGenBuffers(size)
        elif size == 1:
            self.buffers = [GL.glGenBuffers(1)]
        else:
            # TODO : Error, attributes doit etre nul
            print("Error")

        self.glid = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.glid)

        for number, data in enumerate(attributes):
            GL.glEnableVertexAttribArray(number)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[number])
            GL.glBufferData(GL.GL_ARRAY_BUFFER, data, GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(number, 3, GL.GL_FLOAT, False, 0, None)

        if index is not None:
            self.buffers += [GL.glGenBuffers(1)]
            GL.glEnableVertexAttribArray(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[-1])
            GL.glBufferData(GL.GL_ARRAY_BUFFER, index, GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, False, 0, None)        # describe array unit as 2 floats

        GL.glBindVertexArray(0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)

    def draw(self, primitive=GL.GL_TRIANGLES):        
        GL.glBindVertexArray(self.glid)                                         # activate our vertex array

        if self.index :
            GL.glDrawElements(primitive, self.index.size, GL.GL_UNSIGNED_INT, None)  # 9 indexed verts = 3 triangles
        else :
            GL.glDrawArrays(primitive, 0, 3)

        GL.glBindVertexArray(0)

    def __del__(self):
        GL.glDeleteVertexArrays(1, [self.glid])
        # We get the len with len(self.buffers), because the size could change
        GL.glDeleteBuffers(len(self.buffers), self.buffers)
