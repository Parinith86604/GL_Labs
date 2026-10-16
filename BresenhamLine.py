import glfw
from OpenGL.GL import *

if not glfw.init():
    raise Exception("GLFW Failed")

window=glfw.create_window(800,600,"Point",None,None)

if not window:
    glfw.terminate()
    raise Exception("Window Failed")

glfw.make_context_current(window)

while not glfw.window_should_close(window):
    glClearColor(0,0,0,1)
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(10)
    glBegin(GL_LINES)
    glColor3f(1,0,0)
    glVertex2f(-0.5, 0)
    glVertex2f(0.5, 0)
    # glVertex2f(0, 0.5)
    glVertex2f(-0.5,-0.5)
    glVertex2f(0.5,-0.5)
    # glVertex2f(-0.8, -0.8)
    # glVertex2f(-0.4, -0.4)
    # glVertex2f(0.0, 0.0)
    # glVertex2f(0.4, 0.4)
    # glVertex2f(0.8, 0.8)
    glEnd()
    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()