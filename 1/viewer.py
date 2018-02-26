#!/usr/bin/env python3
"""
Python OpenGL practical application.
"""
# Python built-in modules
import os                           # os function, i.e. checking file status

# External, non built-in modules
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args
from test.hello_world import helloo

# Internal modules
from transform import translate, rotate, scale, vec, frustum, perspective

# ------------ low level OpenGL object wrappers ----------------------------
class Shader:
    """ Helper class to create and automatically destroy shader program """
    @staticmethod
    def _compile_shader(src, shader_type):
        src = open(src, 'r').read() if os.path.exists(src) else src
        src = src.decode('ascii') if isinstance(src, bytes) else src
        shader = GL.glCreateShader(shader_type)
        GL.glShaderSource(shader, src)
        GL.glCompileShader(shader)
        status = GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS)
        src = ('%3d: %s' % (i+1, l) for i, l in enumerate(src.splitlines()))
        if not status:
            log = GL.glGetShaderInfoLog(shader).decode('ascii')
            GL.glDeleteShader(shader)
            src = '\n'.join(src)
            print('Compile failed for %s\n%s\n%s' % (shader_type, log, src))
            return None
        return shader

    def __init__(self, vertex_source, fragment_source):
        """ Shader can be initialized with raw strings or source file names """
        self.glid = None
        vert = self._compile_shader(vertex_source, GL.GL_VERTEX_SHADER)
        frag = self._compile_shader(fragment_source, GL.GL_FRAGMENT_SHADER)
        if vert and frag:
            self.glid = GL.glCreateProgram()  # pylint: disable=E1111
            GL.glAttachShader(self.glid, vert)
            GL.glAttachShader(self.glid, frag)
            GL.glLinkProgram(self.glid)
            GL.glDeleteShader(vert)
            GL.glDeleteShader(frag)
            status = GL.glGetProgramiv(self.glid, GL.GL_LINK_STATUS)
            if not status:
                print(GL.glGetProgramInfoLog(self.glid).decode('ascii'))
                GL.glDeleteProgram(self.glid)
                self.glid = None

    def __del__(self):
        GL.glUseProgram(0)
        if self.glid:                      # if this is a valid shader object
            GL.glDeleteProgram(self.glid)  # object dies => destroy GL object


# ------------  Simple color shaders ------------------------------------------
COLOR_VERT = """#version 330 core
uniform mat4 matrix;
layout(location = 0) in vec3 position_in;
layout(location = 1) in vec3 colors_in;
out vec3 position_out;
out vec3 colors_out;
void main() {
    gl_Position = matrix*vec4(position_in, 1);
    position_out = position_in;
    colors_out = colors_in;
}"""

COLOR_FRAG_MULTIPLE = """#version 330 core
uniform vec3 color;
out vec4 outColor;
in vec3 position_out;
in vec3 colors_out;
void main() {
    outColor = vec4(colors_out, 1);
}"""

COLOR_FRAG_UNIFORM = """#version 330 core
uniform vec3 color;
out vec4 outColor;
in vec3 position_out;
in vec3 colors_out;
void main() {
    outColor = vec4(color, 1);
}"""


# ------------  Scene object classes ------------------------------------------
class PyramideMultiColors:
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

class PyramideUniform:
    """Pyramid with uniform colors"""

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
                                perspective(35, 640/480, 0.001, 100)@translate(0.2,0,-1)@rotate(vec(0, 1, 0), -rotater)@scale(scaler))
        GL.glBindVertexArray(self.glid)                                         # activate our vertex array
        GL.glDrawElements(GL.GL_TRIANGLES, self.index.size, GL.GL_UNSIGNED_INT, None)  # 9 indexed verts = 3 triangles

    def __del__(self):
        GL.glDeleteVertexArrays(1, [self.glid])
        GL.glDeleteBuffers(1, self.buffers)


# ------------  Viewer class & window management ------------------------------
class Viewer:
    """ GLFW viewer window, with classic initialization & graphics loop """

    def __init__(self, width=640, height=480):

        # version hints: create GL window with >= OpenGL 3.3 and core profile
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, False)
        self.win = glfw.create_window(width, height, 'Viewer', None, None)

        # make win's OpenGL context current; no OpenGL calls can happen before
        glfw.make_context_current(self.win)

        # register event handlers
        glfw.set_key_callback(self.win, self.on_key)

        # useful message to check OpenGL renderer characteristics
        print('OpenGL', GL.glGetString(GL.GL_VERSION).decode() + ', GLSL',
              GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode() +
              ', Renderer', GL.glGetString(GL.GL_RENDERER).decode())

        # initialize GL by setting viewport and default render characteristics
        GL.glClearColor(0.1, 0.1, 0.1, 0.1)

        GL.glEnable(GL.GL_CULL_FACE)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDepthFunc(GL.GL_LESS)

        # compile and initialize shader programs once globally
        self.multiple_color_shader = Shader(COLOR_VERT, COLOR_FRAG_MULTIPLE)
        self.uniform_color_shader = Shader(COLOR_VERT, COLOR_FRAG_UNIFORM)

        # initially empty list of object to draw
        self.drawables = []

        self.color = (0, 0, 0)

        self.scaler = 0.1
        self.rotater = 2

    def run(self):
        """ Main render loop for this OpenGL window """
        while not glfw.window_should_close(self.win):
            # clear draw buffer
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT);

            # draw our scene objects
            for drawable in self.drawables:
                if(type(drawable) is PyramideMultiColors):
                    drawable.draw(None, None, None, self.multiple_color_shader, self.color,
                                self.scaler, self.rotater)
                else :
                    drawable.draw(None, None, None, self.uniform_color_shader, self.color,
                    self.scaler, self.rotater)

            # flush render commands, and swap draw buffers
            glfw.swap_buffers(self.win)

            # Poll for and process events
            glfw.poll_events()

    def add(self, *drawables):
        """ add objects to draw in this window """
        self.drawables.extend(drawables)

    def on_key(self, _win, key, _scancode, action, _mods):
        """ 'Q' or 'Escape' quits """
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_ESCAPE or key == glfw.KEY_Q:
                glfw.set_window_should_close(self.win, True)
            elif key == glfw.KEY_R:
                self.rotater += 2
            elif key == glfw.KEY_I:
                self.scaler -= 0.05
            elif key == glfw.KEY_O:
                self.scaler += 0.05
            elif key == glfw.KEY_ENTER:
                r, g, b = self.color
                g += 0.1
                self.color = (r, g, b)

# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()

    # place instances of our basic objects
    viewer.add(PyramideMultiColors())
    viewer.add(PyramideUniform())

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    helloo()
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
