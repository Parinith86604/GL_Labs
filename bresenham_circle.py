import glfw
from OpenGL.GL import *

WIDTH = 800
HEIGHT = 600

def plot(x, y):
    glVertex2f((x / WIDTH) * 2 - 1,
               (y / HEIGHT) * 2 - 1)

def drawCirclePoints(xc, yc, x, y):

    plot(xc+x, yc+y)
    plot(xc-x, yc+y)
    plot(xc+x, yc-y)
    plot(xc-x, yc-y)

    plot(xc+y, yc+x)
    plot(xc-y, yc+x)
    plot(xc+y, yc-x)
    plot(xc-y, yc-x)

def bresenhamCircle(xc, yc, r):

    x = 0
    y = r

    d = 3 - 2*r

    glBegin(GL_POINTS)

    while x <= y:

        drawCirclePoints(xc, yc, x, y)

        if d < 0:
            d = d + 4*x + 6
        else:
            d = d + 4*(x-y) + 10
            y -= 1

        x += 1

    glEnd()

if not glfw.init():
    raise Exception("GLFW failed")

window = glfw.create_window(WIDTH, HEIGHT, "Bresenham Circle", None, None)
glfw.make_context_current(window)

while not glfw.window_should_close(window):

    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(0,1,0)

    bresenhamCircle(400,300,150)

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()