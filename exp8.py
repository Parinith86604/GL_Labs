
import glfw
import numpy as np
import ctypes

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


# -------------------- VERTEX SHADER --------------------
VERTEX_SHADER = """
#version 330 core

layout(location = 0) in vec2 aPos;
layout(location = 1) in vec3 aColor;

uniform mat3 transform;

out vec3 vertexColor;

void main()
{
    vec3 position = transform * vec3(aPos, 1.0);
    gl_Position = vec4(position.xy, 0.0, 1.0);
    vertexColor = aColor;
}
"""


# -------------------- FRAGMENT SHADER --------------------
FRAGMENT_SHADER = """
#version 330 core

in vec3 vertexColor;
out vec4 FragColor;

void main()
{
    FragColor = vec4(vertexColor, 1.0);
}
"""


# -------------------- TRANSFORMATION MATRICES --------------------

def translation(tx, ty):
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ], dtype=np.float32)


def rotation(angle):
    c = np.cos(angle)
    s = np.sin(angle)

    return np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ], dtype=np.float32)


def scaling(sx, sy):
    return np.array([
        [sx, 0,  0],
        [0,  sy, 0],
        [0,  0,  1]
    ], dtype=np.float32)


def shear_x(value):
    return np.array([
        [1, value, 0],
        [0, 1,     0],
        [0, 0,     1]
    ], dtype=np.float32)


def shear_y(value):
    return np.array([
        [1,     0, 0],
        [value, 1, 0],
        [0,     0, 1]
    ], dtype=np.float32)


def reflect_x():
    # Reflection about the X-axis
    return scaling(1, -1)


def reflect_y():
    # Reflection about the Y-axis
    return scaling(-1, 1)


# -------------------- MAIN PROGRAM --------------------

def main():
    global_transform = np.identity(3, dtype=np.float32)

    # Initialize GLFW
    if not glfw.init():
        print("Error: GLFW initialization failed.")
        return

    # Request OpenGL 3.3 Core Profile
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(
        glfw.OPENGL_PROFILE,
        glfw.OPENGL_CORE_PROFILE
    )

    # Create window
    window = glfw.create_window(
        800, 600,
        "Experiment 8 - 2D Transformations",
        None, None
    )

    if not window:
        print("Error: Could not create OpenGL window.")
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    glViewport(0, 0, 800, 600)

    try:
        # Compile and link shaders
        shader_program = compileProgram(
            compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
            compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
        )

        # Square made from two triangles.
        # Each vertex contains x, y, red, green, blue.
        vertices = np.array([
            -0.25, -0.25, 1.0, 0.0, 0.0,
             0.25, -0.25, 0.0, 1.0, 0.0,
             0.25,  0.25, 0.0, 0.0, 1.0,

            -0.25, -0.25, 1.0, 0.0, 0.0,
             0.25,  0.25, 0.0, 0.0, 1.0,
            -0.25,  0.25, 1.0, 1.0, 0.0
        ], dtype=np.float32)

        # Create Vertex Array Object and Vertex Buffer Object
        VAO = glGenVertexArrays(1)
        VBO = glGenBuffers(1)

        glBindVertexArray(VAO)

        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(
            GL_ARRAY_BUFFER,
            vertices.nbytes,
            vertices,
            GL_STATIC_DRAW
        )

        stride = 5 * vertices.itemsize

        # Position attribute: x and y
        glVertexAttribPointer(
            0, 2, GL_FLOAT, GL_FALSE,
            stride, ctypes.c_void_p(0)
        )
        glEnableVertexAttribArray(0)

        # Color attribute: red, green and blue
        glVertexAttribPointer(
            1, 3, GL_FLOAT, GL_FALSE,
            stride, ctypes.c_void_p(2 * vertices.itemsize)
        )
        glEnableVertexAttribArray(1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        # Get transformation uniform location
        transform_location = glGetUniformLocation(
            shader_program, "transform"
        )

        # -------------------- KEYBOARD CONTROLS --------------------

        def key_callback(window, key, scancode, action, mods):
            nonlocal global_transform

            if action != glfw.PRESS:
                return

            operation = None

            # Exit
            if key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(window, True)

            # Translation
            elif key == glfw.KEY_LEFT:
                operation = translation(-0.05, 0)
            elif key == glfw.KEY_RIGHT:
                operation = translation(0.05, 0)
            elif key == glfw.KEY_UP:
                operation = translation(0, 0.05)
            elif key == glfw.KEY_DOWN:
                operation = translation(0, -0.05)

            # Rotation
            elif key == glfw.KEY_Q:
                operation = rotation(np.radians(10))
            elif key == glfw.KEY_E:
                operation = rotation(np.radians(-10))

            # Non-uniform scaling
            elif key == glfw.KEY_1:
                operation = scaling(1.1, 1.0)
            elif key == glfw.KEY_2:
                operation = scaling(0.9, 1.0)
            elif key == glfw.KEY_3:
                operation = scaling(1.0, 1.1)
            elif key == glfw.KEY_4:
                operation = scaling(1.0, 0.9)

            # Reflection
            elif key == glfw.KEY_R:
                operation = reflect_x()
            elif key == glfw.KEY_F:
                operation = reflect_y()

            # Shearing
            elif key == glfw.KEY_H:
                operation = shear_x(0.2)
            elif key == glfw.KEY_V:
                operation = shear_y(0.2)

            # Reset
            elif key == glfw.KEY_SPACE:
                global_transform = np.identity(
                    3, dtype=np.float32
                )

            # Apply the selected transformation
            if operation is not None:
                global_transform = operation @ global_transform

        glfw.set_key_callback(window, key_callback)

        print("\nEXPERIMENT 8: 2D GEOMETRIC TRANSFORMATIONS")
        print("------------------------------------------")
        print("Arrow keys : Translation")
        print("Q / E      : Rotate counterclockwise / clockwise")
        print("1 / 2      : Increase / decrease X scaling")
        print("3 / 4      : Increase / decrease Y scaling")
        print("R          : Reflection about X-axis")
        print("F          : Reflection about Y-axis")
        print("H          : Horizontal shearing")
        print("V          : Vertical shearing")
        print("SPACE      : Reset transformations")
        print("ESC        : Exit\n")

        # -------------------- RENDERING LOOP --------------------

        while not glfw.window_should_close(window):
            glClearColor(0.1, 0.1, 0.1, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)

            glUseProgram(shader_program)

            # Send the 3x3 transformation matrix to the vertex shader.
            # GL_TRUE transposes the row-major NumPy matrix for OpenGL.
            glUniformMatrix3fv(
                transform_location,
                1,
                GL_TRUE,
                global_transform
            )

            glBindVertexArray(VAO)
            glDrawArrays(GL_TRIANGLES, 0, 6)

            glfw.swap_buffers(window)
            glfw.poll_events()

        # -------------------- CLEANUP --------------------

        glBindVertexArray(0)
        glUseProgram(0)

        glDeleteVertexArrays(1, [VAO])
        glDeleteBuffers(1, [VBO])
        glDeleteProgram(shader_program)

    except Exception as error:
        print("OpenGL program error:", error)

    finally:
        glfw.terminate()


if __name__ == "__main__":
    main()
