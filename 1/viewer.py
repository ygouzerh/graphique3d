#!/usr/bin/env python3
"""
General viewer
"""
import glfw                         # lean window system wrapper for OpenGL
import OpenGL.GL as GL              # standard Python OpenGL wrapper
from itertools import cycle
from shader import Shader
from shaders_glsl import COLOR_VERT, COLOR_FRAG_MULTIPLE, COLOR_FRAG_UNIFORM
# Internal modules
from transform import Trackball, translate, rotate, scale, vec, frustum, perspective, identity
from pyramids import PyramidMultiColors, PyramidColored

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

        # initialize trackball
        self.trackball = GLFWTrackball(self.win)

        # cyclic iterator to easily toggle polygon rendering modes
        self.fill_modes = cycle([GL.GL_LINE, GL.GL_POINT, GL.GL_FILL])

        self.color = (0, 0, 0)

        self.scaler = 0.1
        self.rotater = 2

    def run(self):
        """ Main render loop for this OpenGL window """
        while not glfw.window_should_close(self.win):

            # clear draw buffer
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT);

            # Create matrix
            winsize = glfw.get_window_size(self.win)
            view = self.trackball.view_matrix()
            projection = self.trackball.projection_matrix(winsize)
            model = identity()

            # draw our scene objects
            for drawable in self.drawables:
                if(type(drawable) is PyramidMultiColors):
                    drawable.draw(projection, view, model, self.multiple_color_shader)
                else :
                    drawable.draw(projection, view, model, self.multiple_color_shader)

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
            elif key == glfw.KEY_W:
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, next(self.fill_modes))

class GLFWTrackball(Trackball):
    """ Use in Viewer for interactive viewpoint control """

    def __init__(self, win):
        """ Init needs a GLFW window handler 'win' to register callbacks """
        super().__init__()
        self.mouse = (0, 0)
        glfw.set_cursor_pos_callback(win, self.on_mouse_move)
        glfw.set_scroll_callback(win, self.on_scroll)

    def on_mouse_move(self, win, xpos, ypos):
        """ Rotate on left-click & drag, pan on right-click & drag """
        old = self.mouse
        self.mouse = (xpos, glfw.get_window_size(win)[1] - ypos)
        if glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_LEFT):
            self.drag(old, self.mouse, glfw.get_window_size(win))
        if glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_RIGHT):
            self.pan(old, self.mouse)

    def on_scroll(self, win, _deltax, deltay):
        """ Scroll controls the camera distance to trackball center """
        self.zoom(deltay, glfw.get_window_size(win)[1])
