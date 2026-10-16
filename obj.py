import glfw
from OpenGL.GL import *
import time

# Initialize GLFW
if not glfw.init():
    raise Exception("GLFW initialization failed")

# Create window
window = glfw.create_window(800, 600, "Moving Square", None, None)

if not window:
    glfw.terminate()
    raise Exception("Window creation failed")

glfw.make_context_current(window)

# Square position
x = -0.8
speed = 0.01

while not glfw.window_should_close(window):

    # Background color
    glClearColor(0.1, 0.1, 0.15, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # Move square
    x += speed

    # Bounce back
    if x > 0.8 or x < -0.8:
        speed = -speed

    # Draw square
    glBegin(GL_QUADS)

    glColor3f(0.0, 1.0, 0.0)      # Green

    glVertex2f(x - 0.1, -0.1)
    glVertex2f(x + 0.1, -0.1)
    glVertex2f(x + 0.1,  0.1)
    glVertex2f(x - 0.1,  0.1)

    glEnd()

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()