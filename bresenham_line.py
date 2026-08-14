import glfw
from OpenGL.GL import *

WIDTH, HEIGHT = 800, 600

# Convert pixel coordinates to OpenGL coordinates
def plot(x, y):
    glVertex2f((x / WIDTH) * 2 - 1,
               (y / HEIGHT) * 2 - 1)

def bresenham(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1

    err = dx - dy

    glBegin(GL_POINTS)

    while True:
        plot(x1, y1)

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * err

        if e2 > -dy:
            err -= dy
            x1 += sx

        if e2 < dx:
            err += dx
            y1 += sy

    glEnd()

if not glfw.init():
    raise Exception("GLFW failed")

window = glfw.create_window(WIDTH, HEIGHT, "Bresenham Line", None, None)
glfw.make_context_current(window)

while not glfw.window_should_close(window):

    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(1, 1, 1)

    bresenham(100, 100, 700, 500)

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()