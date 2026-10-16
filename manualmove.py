import glfw
from OpenGL.GL import *

# Initialize GLFW
if not glfw.init():
    raise Exception("GLFW initialization failed")

window = glfw.create_window(800, 600, "Snake Style Movement", None, None)

if not window:
    glfw.terminate()
    raise Exception("Window creation failed")

glfw.make_context_current(window)

# Square position
x = 0.0
y = 0.0

# One movement step
STEP = 0.1

# To detect a single key press
prev_left = prev_right = prev_up = prev_down = glfw.RELEASE

while not glfw.window_should_close(window):

    left = glfw.get_key(window, glfw.KEY_LEFT)
    right = glfw.get_key(window, glfw.KEY_RIGHT)
    up = glfw.get_key(window, glfw.KEY_UP)
    down = glfw.get_key(window, glfw.KEY_DOWN)

    # Move only once per key press
    if left == glfw.PRESS and prev_left == glfw.RELEASE:
        x -= STEP

    if right == glfw.PRESS and prev_right == glfw.RELEASE:
        x += STEP

    if up == glfw.PRESS and prev_up == glfw.RELEASE:
        y += STEP

    if down == glfw.PRESS and prev_down == glfw.RELEASE:
        y -= STEP

    prev_left = left
    prev_right = right
    prev_up = up
    prev_down = down

    # Draw
    glClearColor(0.1, 0.1, 0.15, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_QUADS)

    glColor3f(0.0, 1.0, 0.0)

    glVertex2f(x - 0.1, y - 0.1)
    glVertex2f(x + 0.1, y - 0.1)
    glVertex2f(x + 0.1, y + 0.1)
    glVertex2f(x - 0.1, y + 0.1)

    glEnd()

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()