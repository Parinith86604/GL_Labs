# EXPERIMENT 10
# 3D Viewing Pipeline: Projection and Viewport Mapping
# Note: The supplied experiment title describes 3D viewing, while its aim
# and objectives describe 2D geometric transformations.

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math


# Cube vertices
vertices = [
    (-1, -1, -1),
    ( 1, -1, -1),
    ( 1,  1, -1),
    (-1,  1, -1),
    (-1, -1,  1),
    ( 1, -1,  1),
    ( 1,  1,  1),
    (-1,  1,  1)
]

# Cube faces and their colors
faces = [
    ((0, 1, 2, 3), (1.0, 0.0, 0.0)),
    ((4, 5, 6, 7), (0.0, 1.0, 0.0)),
    ((0, 1, 5, 4), (0.0, 0.0, 1.0)),
    ((2, 3, 7, 6), (1.0, 1.0, 0.0)),
    ((0, 3, 7, 4), (1.0, 0.0, 1.0)),
    ((1, 2, 6, 5), (0.0, 1.0, 1.0))
]


def draw_cube():
    glBegin(GL_QUADS)

    for face, color in faces:
        glColor3f(*color)

        for vertex_index in face:
            glVertex3f(*vertices[vertex_index])

    glEnd()


def draw_axes():
    glLineWidth(2.0)
    glBegin(GL_LINES)

    # X-axis: red
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-2.0, 0.0, 0.0)
    glVertex3f( 2.0, 0.0, 0.0)

    # Y-axis: green
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -2.0, 0.0)
    glVertex3f(0.0,  2.0, 0.0)

    # Z-axis: blue
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -2.0)
    glVertex3f(0.0, 0.0,  2.0)

    glEnd()


def setup_camera_perspective(width, height):
    aspect = width / float(max(height, 1))

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, aspect, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(
        4.0, 3.0, 6.0,
        0.0, 0.0, 0.0,
        0.0, 1.0, 0.0
    )


def setup_camera_orthographic(width, height):
    aspect = width / float(max(height, 1))

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(
        -2.5 * aspect, 2.5 * aspect,
        -2.5, 2.5,
        0.1, 100.0
    )

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(
        4.0, 3.0, 6.0,
        0.0, 0.0, 0.0,
        0.0, 1.0, 0.0
    )


def main():
    if not glfw.init():
        print("Failed to initialize GLFW.")
        return

    # Request a compatibility context for immediate-mode OpenGL.
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)

    window = glfw.create_window(
        1000, 600,
        "Experiment 10 - 3D Viewing Pipeline",
        None, None
    )

    if not window:
        glfw.terminate()
        print("Failed to create the OpenGL window.")
        return

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.08, 0.08, 0.12, 1.0)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        framebuffer_width, framebuffer_height = (
            glfw.get_framebuffer_size(window)
        )

        if framebuffer_width == 0 or framebuffer_height == 0:
            continue

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Automatic rotation
        angle = glfw.get_time() * 45.0

        # Split the window into two viewports.
        left_width = framebuffer_width // 2
        right_width = framebuffer_width - left_width

        # -------------------------------------------------
        # LEFT VIEWPORT: Perspective Projection
        # -------------------------------------------------
        glViewport(0, 0, left_width, framebuffer_height)

        setup_camera_perspective(left_width, framebuffer_height)

        glPushMatrix()
        glRotatef(angle, 0.0, 1.0, 0.0)
        glRotatef(20.0, 1.0, 0.0, 0.0)
        draw_axes()
        draw_cube()
        glPopMatrix()

        # -------------------------------------------------
        # RIGHT VIEWPORT: Orthographic Projection
        # -------------------------------------------------
        glViewport(
            left_width, 0,
            right_width, framebuffer_height
        )

        setup_camera_orthographic(right_width, framebuffer_height)

        glPushMatrix()
        glRotatef(angle, 0.0, 1.0, 0.0)
        glRotatef(20.0, 1.0, 0.0, 0.0)
        draw_axes()
        draw_cube()
        glPopMatrix()

        glfw.swap_buffers(window)

    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == "__main__":
    main()