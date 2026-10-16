import sys
import glfw
from OpenGL.GL import *

z_buffer_enabled = True


def handle_key(window, key, scancode, action, mods):
    global z_buffer_enabled

    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)

        elif key == glfw.KEY_SPACE:
            z_buffer_enabled = not z_buffer_enabled
            state = "ON" if z_buffer_enabled else "OFF"
            print("Z-buffer depth testing:", state)


def draw_front_triangle():
    # Nearer red triangle
    glColor3f(1.0, 0.2, 0.16)

    glBegin(GL_TRIANGLES)
    glVertex3f(-0.58, -0.38, 0.55)
    glVertex3f(0.62, -0.30, 0.55)
    glVertex3f(0.05, 0.66, 0.55)
    glEnd()


def draw_back_triangle():
    # Farther blue triangle
    glColor3f(0.12, 0.52, 1.0)

    glBegin(GL_TRIANGLES)
    glVertex3f(-0.82, -0.62, -0.55)
    glVertex3f(0.82, -0.62, -0.55)
    glVertex3f(0.00, 0.82, -0.55)
    glEnd()


def set_projection(width, height):
    width = max(width, 1)
    height = max(height, 1)
    aspect = width / height

    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if aspect >= 1:
        glOrtho(-aspect, aspect, -1, 1, -5, 5)
    else:
        glOrtho(-1, 1, -1 / aspect, 1 / aspect, -5, 5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    global z_buffer_enabled

    if not glfw.init():
        print("Error: GLFW initialization failed.")
        return 1

    # Request an OpenGL context with a depth buffer.
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.DEPTH_BITS, 24)
    glfw.window_hint(glfw.DOUBLEBUFFER, glfw.TRUE)

    window = glfw.create_window(
        800, 600,
        "Experiment 6 - Z-Buffer",
        None, None
    )

    if window is None:
        glfw.terminate()
        print("Error: Could not create OpenGL window.")
        return 1

    glfw.make_context_current(window)
    glfw.swap_interval(1)
    glfw.set_key_callback(window, handle_key)

    glClearColor(0.055, 0.065, 0.09, 1.0)
    glClearDepth(1.0)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    print("Z-Buffer Algorithm for Hidden Surface Removal")
    print("SPACE: Toggle depth testing")
    print("ESC: Exit")
    print("Z-buffer depth testing: ON")

    while not glfw.window_should_close(window):
        width, height = glfw.get_framebuffer_size(window)
        set_projection(width, height)

        # Clear both the color buffer and the depth buffer.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if z_buffer_enabled:
            glEnable(GL_DEPTH_TEST)
            glDepthFunc(GL_LESS)
        else:
            glDisable(GL_DEPTH_TEST)

        # Draw the near object first and the far object second.
        draw_front_triangle()
        draw_back_triangle()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.destroy_window(window)
    glfw.terminate()
    return 0


if __name__ == "__main__":
    sys.exit(main())