from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Original triangle vertices
triangle = [
    [0.0, 0.0, 1.0],
    [0.5, 0.0, 1.0],
    [0.25, 0.5, 1.0]
]


# Matrix multiplication
def multiply_matrix(A, B):
    result = [[0, 0, 0] for _ in range(3)]

    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[i][j] += A[i][k] * B[k][j]

    return result


# Apply transformation matrix to a point
def transform_point(matrix, point):
    result = [0, 0, 0]

    for i in range(3):
        for j in range(3):
            result[i] += matrix[i][j] * point[j]

    return result


# Draw triangle
def draw_triangle(vertices):
    glBegin(GL_TRIANGLES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(vertices[0][0], vertices[0][1])

    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(vertices[1][0], vertices[1][1])

    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(vertices[2][0], vertices[2][1])

    glEnd()


# Create transformation matrices
def create_transformations():

    # Translation matrix
    tx = 0.7
    ty = 0.4

    T = [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]

    # Rotation matrix
    angle = math.radians(45)

    R = [
        [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ]

    # Scaling matrix
    sx = 1.5
    sy = 1.5

    S = [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ]

    # Composite transformation
    RS = multiply_matrix(R, S)
    TRS = multiply_matrix(T, RS)

    return TRS


# Display function
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # Draw original triangle
    glColor3f(0.5, 0.5, 0.5)
    draw_triangle(triangle)

    # Get composite transformation matrix
    transformation_matrix = create_transformations()

    # Transform triangle
    transformed_triangle = []

    for point in triangle:
        new_point = transform_point(transformation_matrix, point)
        transformed_triangle.append(new_point)

    # Draw transformed triangle
    draw_triangle(transformed_triangle)

    glFlush()


# Initialization
def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluOrtho2D(-1.0, 2.0, -1.0, 2.0)

    glMatrixMode(GL_MODELVIEW)


# Main function
def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)

    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)

    glutCreateWindow(
        b"Experiment 4 - Composite Transformations"
    )

    init()

    glutDisplayFunc(display)

    glutMainLoop()


if __name__ == "__main__":
    main()