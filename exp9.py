import ctypes
import glfw
import numpy as np

from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram


# Vertex Shader
VERTEX_SHADER = """
#version 330 core

layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 vertexColor;

void main()
{
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    vertexColor = aColor;
}
"""


# Fragment Shader
FRAGMENT_SHADER = """
#version 330 core

in vec3 vertexColor;
out vec4 FragColor;

void main()
{
    FragColor = vec4(vertexColor, 1.0);
}
"""


# Transformation State
state = {
    "position": np.array([0.0, 0.0, 0.0], dtype=np.float32),
    "rotation": np.array([0.0, 0.0, 0.0], dtype=np.float32),
    "scale": 1.0
}


# Reset Object
def reset_object():
    state["position"][:] = [0.0, 0.0, 0.0]
    state["rotation"][:] = [0.0, 0.0, 0.0]
    state["scale"] = 1.0


# Keyboard Callback
def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_R and action == glfw.PRESS:
        reset_object()


# Translation Matrix
def translation_matrix(x, y, z):
    matrix = np.identity(4, dtype=np.float32)
    matrix[0, 3] = x
    matrix[1, 3] = y
    matrix[2, 3] = z
    return matrix


# Scaling Matrix
def scaling_matrix(s):
    return np.array([
        [s, 0, 0, 0],
        [0, s, 0, 0],
        [0, 0, s, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)


# Rotation Around X-Axis
def rotation_x(angle):
    c = np.cos(angle)
    s = np.sin(angle)

    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)


# Rotation Around Y-Axis
def rotation_y(angle):
    c = np.cos(angle)
    s = np.sin(angle)

    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)


# Rotation Around Z-Axis
def rotation_z(angle):
    c = np.cos(angle)
    s = np.sin(angle)

    return np.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)


# Perspective Projection Matrix
def perspective(fov, aspect, near, far):
    f = 1.0 / np.tan(np.radians(fov) / 2.0)

    return np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far),
         (2 * far * near) / (near - far)],
        [0, 0, -1, 0]
    ], dtype=np.float32)


# Camera View Matrix
def look_at(eye, target, up):
    forward = target - eye
    forward = forward / np.linalg.norm(forward)

    right = np.cross(forward, up)
    right = right / np.linalg.norm(right)

    camera_up = np.cross(right, forward)

    return np.array([
        [right[0], right[1], right[2],
         -np.dot(right, eye)],

        [camera_up[0], camera_up[1], camera_up[2],
         -np.dot(camera_up, eye)],

        [-forward[0], -forward[1], -forward[2],
         np.dot(forward, eye)],

        [0, 0, 0, 1]
    ], dtype=np.float32)


# Upload Matrix to OpenGL
def set_matrix(location, matrix):
    glUniformMatrix4fv(
        location,
        1,
        GL_FALSE,
        np.ascontiguousarray(matrix.T, dtype=np.float32)
    )


# Create Vertex Buffer
def create_mesh(vertices):
    vertices = np.asarray(vertices, dtype=np.float32)

    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    glBufferData(
        GL_ARRAY_BUFFER,
        vertices.nbytes,
        vertices,
        GL_STATIC_DRAW
    )

    stride = 6 * ctypes.sizeof(ctypes.c_float)

    glVertexAttribPointer(
        0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0)
    )
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(
        1, 3, GL_FLOAT, GL_FALSE, stride,
        ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float))
    )
    glEnableVertexAttribArray(1)

    glBindVertexArray(0)

    return vao, vbo, len(vertices)


# Generate a Multicolored Cube
def create_cube():
    p = {
        "000": (-0.7, -0.7, -0.7),
        "100": ( 0.7, -0.7, -0.7),
        "110": ( 0.7,  0.7, -0.7),
        "010": (-0.7,  0.7, -0.7),
        "001": (-0.7, -0.7,  0.7),
        "101": ( 0.7, -0.7,  0.7),
        "111": ( 0.7,  0.7,  0.7),
        "011": (-0.7,  0.7,  0.7)
    }

    faces = [
        (["001", "101", "111", "011"], (1.0, 0.2, 0.2)),
        (["100", "000", "010", "110"], (0.2, 1.0, 0.2)),
        (["101", "100", "110", "111"], (0.2, 0.4, 1.0)),
        (["000", "001", "011", "010"], (1.0, 1.0, 0.2)),
        (["011", "111", "110", "010"], (1.0, 0.2, 1.0)),
        (["000", "100", "101", "001"], (0.2, 1.0, 1.0))
    ]

    vertices = []

    for corners, color in faces:
        points = [p[key] for key in corners]

        for index in (0, 1, 2, 0, 2, 3):
            vertices.extend(points[index])
            vertices.extend(color)

    return vertices


# Generate Ground Grid
def create_grid():
    vertices = []

    for i in range(-10, 11):
        coordinate = float(i)

        if i == 0:
            x_color = (0.9, 0.25, 0.25)
            z_color = (0.25, 0.45, 1.0)
        else:
            x_color = (0.35, 0.38, 0.43)
            z_color = (0.35, 0.38, 0.43)

        vertices.extend([
            coordinate, -0.72, -10.0, *x_color,
            coordinate, -0.72,  10.0, *x_color
        ])

        vertices.extend([
            -10.0, -0.72, coordinate, *z_color,
             10.0, -0.72, coordinate, *z_color
        ])

    return vertices


# Main Program
def main():
    if not glfw.init():
        print("Error: Could not initialize GLFW.")
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(
        glfw.OPENGL_PROFILE,
        glfw.OPENGL_CORE_PROFILE
    )

    window = glfw.create_window(
        1000, 700,
        "Experiment 9 - Interactive 3D Scene",
        None, None
    )

    if not window:
        glfw.terminate()
        print("Error: Could not create OpenGL window.")
        return

    glfw.make_context_current(window)
    glfw.swap_interval(1)
    glfw.set_key_callback(window, key_callback)

    glEnable(GL_DEPTH_TEST)

    try:
        shader_program = compileProgram(
            compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
            compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
        )
    except Exception as error:
        print("Shader compilation error:", error)
        glfw.terminate()
        return

    glUseProgram(shader_program)

    model_location = glGetUniformLocation(
        shader_program, "model"
    )
    view_location = glGetUniformLocation(
        shader_program, "view"
    )
    projection_location = glGetUniformLocation(
        shader_program, "projection"
    )

    cube_vao, cube_vbo, cube_count = create_mesh(create_cube())
    grid_vao, grid_vbo, grid_count = create_mesh(create_grid())

    eye = np.array([4.0, 3.5, 6.0], dtype=np.float32)
    target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
    up = np.array([0.0, 1.0, 0.0], dtype=np.float32)

    view = look_at(eye, target, up)

    last_time = glfw.get_time()
    move_speed = 3.0
    rotate_speed = 90.0
    scale_speed = 1.0

    print("\n--- Experiment 9: Interactive 3D Scene ---")
    print("W/A/S/D : Move the cube")
    print("I/K     : Rotate around X-axis")
    print("J/L     : Rotate around Y-axis")
    print("U/O     : Rotate around Z-axis")
    print("+/-     : Increase/decrease scale")
    print("R       : Reset object")
    print("ESC     : Exit\n")

    while not glfw.window_should_close(window):
        current_time = glfw.get_time()
        delta_time = min(current_time - last_time, 0.05)
        last_time = current_time

        glfw.poll_events()

        # Object Translation
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            state["position"][2] -= move_speed * delta_time

        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            state["position"][2] += move_speed * delta_time

        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            state["position"][0] -= move_speed * delta_time

        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            state["position"][0] += move_speed * delta_time

        # Object Rotation
        if glfw.get_key(window, glfw.KEY_I) == glfw.PRESS:
            state["rotation"][0] += rotate_speed * delta_time

        if glfw.get_key(window, glfw.KEY_K) == glfw.PRESS:
            state["rotation"][0] -= rotate_speed * delta_time

        if glfw.get_key(window, glfw.KEY_J) == glfw.PRESS:
            state["rotation"][1] -= rotate_speed * delta_time

        if glfw.get_key(window, glfw.KEY_L) == glfw.PRESS:
            state["rotation"][1] += rotate_speed * delta_time

        if glfw.get_key(window, glfw.KEY_U) == glfw.PRESS:
            state["rotation"][2] -= rotate_speed * delta_time

        if glfw.get_key(window, glfw.KEY_O) == glfw.PRESS:
            state["rotation"][2] += rotate_speed * delta_time

        # Object Scaling
        plus_pressed = (
            glfw.get_key(window, glfw.KEY_EQUAL) == glfw.PRESS
            or glfw.get_key(window, glfw.KEY_KP_ADD) == glfw.PRESS
        )

        minus_pressed = (
            glfw.get_key(window, glfw.KEY_MINUS) == glfw.PRESS
            or glfw.get_key(window, glfw.KEY_KP_SUBTRACT) == glfw.PRESS
        )

        if plus_pressed:
            state["scale"] = min(
                3.0, state["scale"] + scale_speed * delta_time
            )

        if minus_pressed:
            state["scale"] = max(
                0.2, state["scale"] - scale_speed * delta_time
            )

        # Build Composite Transformation Matrix
        position = state["position"]
        angles = np.radians(state["rotation"])

        translation = translation_matrix(
            position[0], position[1], position[2]
        )

        rotation = (
            rotation_x(angles[0])
            @ rotation_y(angles[1])
            @ rotation_z(angles[2])
        )

        scaling = scaling_matrix(state["scale"])

        model = translation @ rotation @ scaling

        # Handle Window Resizing
        width, height = glfw.get_framebuffer_size(window)

        if height == 0:
            continue

        glViewport(0, 0, width, height)

        projection = perspective(
            45.0, width / height, 0.1, 100.0
        )

        # Clear Screen
        glClearColor(0.08, 0.09, 0.13, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(shader_program)

        set_matrix(view_location, view)
        set_matrix(projection_location, projection)

        # Draw Ground Grid
        set_matrix(model_location, np.identity(4, dtype=np.float32))
        glBindVertexArray(grid_vao)
        glDrawArrays(GL_LINES, 0, grid_count)

        # Draw Interactive Cube
        set_matrix(model_location, model)
        glBindVertexArray(cube_vao)
        glDrawArrays(GL_TRIANGLES, 0, cube_count)

        glBindVertexArray(0)

        glfw.swap_buffers(window)

    # Release Resources
    glDeleteVertexArrays(1, [cube_vao])
    glDeleteBuffers(1, [cube_vbo])
    glDeleteVertexArrays(1, [grid_vao])
    glDeleteBuffers(1, [grid_vbo])
    glDeleteProgram(shader_program)

    glfw.terminate()


if __name__ == "__main__":
    main()