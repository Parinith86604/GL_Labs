import glfw
from OpenGL.GL import *
import math

# ---------------------------------------------------------
# 2D TRANSFORMATIONS USING HOMOGENEOUS COORDINATES
# ---------------------------------------------------------

# Original triangle vertices in homogeneous coordinates
triangle = [
    [-0.2, -0.2, 1.0],
    [ 0.2, -0.2, 1.0],
    [ 0.0,  0.2, 1.0]
]

# Transformation parameters
tx = 0.0
ty = 0.0
angle = 0.0
sx = 1.0
sy = 1.0
shx = 0.0
shy = 0.0

# Reflection flags
reflect_x = False
reflect_y = False


# ---------------------------------------------------------
# Matrix Multiplication
# ---------------------------------------------------------

def multiply_matrix(A, B):
    result = [[0.0 for _ in range(3)] for _ in range(3)]

    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[i][j] += A[i][k] * B[k][j]

    return result


# ---------------------------------------------------------
# Apply Matrix to Point
# ---------------------------------------------------------

def transform_point(M, P):
    x = M[0][0] * P[0] + M[0][1] * P[1] + M[0][2] * P[2]
    y = M[1][0] * P[0] + M[1][1] * P[1] + M[1][2] * P[2]
    w = M[2][0] * P[0] + M[2][1] * P[1] + M[2][2] * P[2]

    if w != 0:
        x /= w
        y /= w

    return [x, y, 1.0]


# ---------------------------------------------------------
# Transformation Matrices
# ---------------------------------------------------------

def translation_matrix(tx, ty):
    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]


def rotation_matrix(angle):
    rad = math.radians(angle)

    c = math.cos(rad)
    s = math.sin(rad)

    return [
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ]


def scaling_matrix(sx, sy):
    return [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ]


def reflection_x_matrix():
    return [
        [1,  0, 0],
        [0, -1, 0],
        [0,  0, 1]
    ]


def reflection_y_matrix():
    return [
        [-1, 0, 0],
        [0,  1, 0],
        [0,  0, 1]
    ]


def shear_matrix(shx, shy):
    return [
        [1, shx, 0],
        [shy, 1, 0],
        [0, 0, 1]
    ]


# ---------------------------------------------------------
# Print Matrix
# ---------------------------------------------------------

def print_matrix(name, M):

    print("\n" + "=" * 45)
    print(name)
    print("=" * 45)

    for row in M:
        print("[ " + "  ".join(f"{value:7.3f}" for value in row) + " ]")


# ---------------------------------------------------------
# Get Final Transformation Matrix
# ---------------------------------------------------------

def get_transformation_matrix():

    # Translation
    T = translation_matrix(tx, ty)

    # Rotation
    R = rotation_matrix(angle)

    # Scaling
    S = scaling_matrix(sx, sy)

    # Shearing
    H = shear_matrix(shx, shy)

    # Start with Identity Matrix
    M = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]

    # Matrix order:
    # M = T × R × S × H

    M = multiply_matrix(M, T)
    M = multiply_matrix(M, R)
    M = multiply_matrix(M, S)
    M = multiply_matrix(M, H)

    # Reflection
    if reflect_x:
        M = multiply_matrix(M, reflection_x_matrix())

    if reflect_y:
        M = multiply_matrix(M, reflection_y_matrix())

    return M


# ---------------------------------------------------------
# Draw Triangle
# ---------------------------------------------------------

def draw_triangle(vertices, color):

    glColor3f(color[0], color[1], color[2])

    glBegin(GL_TRIANGLES)

    for vertex in vertices:
        glVertex2f(vertex[0], vertex[1])

    glEnd()


# ---------------------------------------------------------
# Display
# ---------------------------------------------------------

def display():

    global triangle

    glClear(GL_COLOR_BUFFER_BIT)

    # -----------------------------------------------------
    # Original Triangle
    # -----------------------------------------------------

    original = []

    for vertex in triangle:
        original.append([
            vertex[0] - 0.6,
            vertex[1],
            1.0
        ])

    draw_triangle(original, (0.6, 0.6, 0.6))

    # -----------------------------------------------------
    # Transformation Matrix
    # -----------------------------------------------------

    M = get_transformation_matrix()

    transformed = []

    for vertex in triangle:
        transformed.append(transform_point(M, vertex))

    # -----------------------------------------------------
    # Draw Transformed Triangle
    # -----------------------------------------------------

    draw_triangle(
        transformed,
        (1.0, 0.0, 0.0)
    )

    glfw.swap_buffers(window)


# ---------------------------------------------------------
# Keyboard Controls
# ---------------------------------------------------------

def key_callback(window, key, scancode, action, mods):

    global tx, ty
    global angle
    global sx, sy
    global shx, shy
    global reflect_x, reflect_y

    if action != glfw.PRESS and action != glfw.REPEAT:
        return

    # ---------------------------------------------
    # Translation
    # ---------------------------------------------

    if key == glfw.KEY_T:
        tx += 0.1

        print("\nTRANSLATION")
        print(f"tx = {tx}, ty = {ty}")
        print_matrix(
            "Translation Matrix",
            translation_matrix(tx, ty)
        )

    # ---------------------------------------------
    # Rotation
    # ---------------------------------------------

    elif key == glfw.KEY_R:
        angle += 10

        print("\nROTATION")
        print(f"Angle = {angle} degrees")
        print_matrix(
            "Rotation Matrix",
            rotation_matrix(angle)
        )

    # ---------------------------------------------
    # Scaling
    # ---------------------------------------------

    elif key == glfw.KEY_S:
        sx += 0.1
        sy += 0.1

        print("\nSCALING")
        print(f"sx = {sx}, sy = {sy}")
        print_matrix(
            "Scaling Matrix",
            scaling_matrix(sx, sy)
        )

    # ---------------------------------------------
    # X Shearing
    # ---------------------------------------------

    elif key == glfw.KEY_X:
        shx += 0.1

        print("\nX-SHEARING")
        print(f"shx = {shx}")

        print_matrix(
            "Shearing Matrix",
            shear_matrix(shx, shy)
        )

    # ---------------------------------------------
    # Y Shearing
    # ---------------------------------------------

    elif key == glfw.KEY_Y:
        shy += 0.1

        print("\nY-SHEARING")
        print(f"shy = {shy}")

        print_matrix(
            "Shearing Matrix",
            shear_matrix(shx, shy)
        )

    # ---------------------------------------------
    # Reflection about X-axis
    # ---------------------------------------------

    elif key == glfw.KEY_1:
        reflect_x = not reflect_x

        print("\nREFLECTION ABOUT X-AXIS")

        print_matrix(
            "Reflection X Matrix",
            reflection_x_matrix()
        )

    # ---------------------------------------------
    # Reflection about Y-axis
    # ---------------------------------------------

    elif key == glfw.KEY_2:
        reflect_y = not reflect_y

        print("\nREFLECTION ABOUT Y-AXIS")

        print_matrix(
            "Reflection Y Matrix",
            reflection_y_matrix()
        )

    # ---------------------------------------------
    # Reset
    # ---------------------------------------------

    elif key == glfw.KEY_0:

        tx = 0.0
        ty = 0.0
        angle = 0.0
        sx = 1.0
        sy = 1.0
        shx = 0.0
        shy = 0.0
        reflect_x = False
        reflect_y = False

        print("\nRESET")
        print("All transformations reset.")

    # ---------------------------------------------
    # Exit
    # ---------------------------------------------

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    glfw.post_empty_event()


# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------

def main():

    global window

    # Initialize GLFW
    if not glfw.init():
        print("Failed to initialize GLFW")
        return

    # Create Window
    window = glfw.create_window(
        800,
        600,
        "Experiment 3 - 2D Transformations",
        None,
        None
    )

    if not window:
        print("Failed to create GLFW window")
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Keyboard callback
    glfw.set_key_callback(window, key_callback)

    # Background
    glClearColor(1.0, 1.0, 1.0, 1.0)

    # Projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glOrtho(
        -1.0, 1.0,
        -1.0, 1.0,
        -1.0, 1.0
    )

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Main Loop
    while not glfw.window_should_close(window):

        glClear(GL_COLOR_BUFFER_BIT)

        glLoadIdentity()

        display()

        glfw.poll_events()

    glfw.terminate()


# ---------------------------------------------------------
# Run Program
# ---------------------------------------------------------

if __name__ == "__main__":
    main()