import glfw
from OpenGL.GL import *


# ============================================================
# PROBLEM 2 - TRANSLATION OF A TRIANGLE
#
# A = (1,1)
# B = (5,2)
# C = (3,6)
#
# tx = 4
# ty = 3
#
# A' = (5,4)
# B' = (9,5)
# C' = (7,9)
# ============================================================


# ------------------------------------------------------------
# Matrix Multiplication
# ------------------------------------------------------------
def multiply(A, B):

    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]

    return result


# ------------------------------------------------------------
# Translation Matrix
# ------------------------------------------------------------
def translation(tx, ty):

    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]


# ------------------------------------------------------------
# Transform Point
# ------------------------------------------------------------
def transform_point(M, x, y):

    point = [
        [x],
        [y],
        [1]
    ]

    result = multiply(M, point)

    return result[0][0], result[1][0]


# ------------------------------------------------------------
# Transform Triangle
# ------------------------------------------------------------
def transform_triangle(M, triangle):

    transformed = []

    for x, y in triangle:

        new_x, new_y = transform_point(
            M,
            x,
            y
        )

        transformed.append(
            (new_x, new_y)
        )

    return transformed


# ------------------------------------------------------------
# Draw Triangle
# ------------------------------------------------------------
def draw_triangle(triangle):

    glBegin(GL_LINE_LOOP)

    for x, y in triangle:

        glVertex2f(
            x / 10.0,
            y / 10.0
        )

    glEnd()


# ------------------------------------------------------------
# Draw Axes
# ------------------------------------------------------------
def draw_axes():

    glColor3f(
        0.5,
        0.5,
        0.5
    )

    glBegin(GL_LINES)

    # X-axis
    glVertex2f(-1.0, 0.0)
    glVertex2f(1.0, 0.0)

    # Y-axis
    glVertex2f(0.0, -1.0)
    glVertex2f(0.0, 1.0)

    glEnd()


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():

    # Original triangle
    triangle = [
        (1, 1),
        (5, 2),
        (3, 6)
    ]

    # Translation values
    tx = 4
    ty = 3

    # Translation matrix
    T = translation(tx, ty)

    # Transform triangle
    transformed = transform_triangle(
        T,
        triangle
    )

    # --------------------------------------------------------
    # Console Output
    # --------------------------------------------------------

    print("\n========================================")
    print("PROBLEM 2 - TRIANGLE TRANSLATION")
    print("========================================")

    print("\nOriginal Triangle:")
    print("A =", triangle[0])
    print("B =", triangle[1])
    print("C =", triangle[2])

    print("\nTranslation:")
    print("tx =", tx)
    print("ty =", ty)

    print("\nTranslation Matrix:")
    print("[ 1   0   4 ]")
    print("[ 0   1   3 ]")
    print("[ 0   0   1 ]")

    print("\nTranslated Triangle:")
    print("A' =", transformed[0])
    print("B' =", transformed[1])
    print("C' =", transformed[2])

    # --------------------------------------------------------
    # OpenGL Initialization
    # --------------------------------------------------------

    if not glfw.init():

        print("GLFW initialization failed")

        return

    window = glfw.create_window(
        800,
        600,
        "Problem 2 - Triangle Translation",
        None,
        None
    )

    if not window:

        glfw.terminate()

        print("Window creation failed")

        return

    glfw.make_context_current(window)

    glClearColor(
        0.0,
        0.0,
        0.0,
        1.0
    )

    # --------------------------------------------------------
    # Display Loop
    # --------------------------------------------------------

    while not glfw.window_should_close(window):

        glClear(
            GL_COLOR_BUFFER_BIT
        )

        # ------------------------------------
        # Coordinate Axes
        # ------------------------------------

        glLineWidth(1)

        draw_axes()

        # ------------------------------------
        # Original Triangle - WHITE
        # ------------------------------------

        glColor3f(
            1.0,
            1.0,
            1.0
        )

        glLineWidth(3)

        draw_triangle(
            triangle
        )

        # ------------------------------------
        # Translated Triangle - RED
        # ------------------------------------

        glColor3f(
            1.0,
            0.0,
            0.0
        )

        glLineWidth(3)

        draw_triangle(
            transformed
        )

        # ------------------------------------
        # Update
        # ------------------------------------

        glfw.swap_buffers(window)

        glfw.poll_events()

    glfw.terminate()


# ------------------------------------------------------------
# Run
# ------------------------------------------------------------

if __name__ == "__main__":

    main()