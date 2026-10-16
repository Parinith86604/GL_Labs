from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# ---------------------------------------------------------
# Cohen-Sutherland Line Clipping Algorithm
# ---------------------------------------------------------

# Region codes
INSIDE = 0       # 0000
LEFT = 1         # 0001
RIGHT = 2        # 0010
BOTTOM = 4       # 0100
TOP = 8          # 1000

# Clipping window
xmin, ymin = 200, 150
xmax, ymax = 600, 450

# Original line coordinates
x1, y1 = 100, 100
x2, y2 = 700, 500


def compute_code(x, y):
    """
    Calculate the 4-bit region code for a point.
    """

    code = INSIDE

    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT

    if y < ymin:
        code |= BOTTOM
    elif y > ymax:
        code |= TOP

    return code


def cohen_sutherland_clip(x1, y1, x2, y2):
    """
    Cohen-Sutherland line clipping algorithm.
    Returns clipped coordinates if the line is accepted.
    Returns None if the line is rejected.
    """

    code1 = compute_code(x1, y1)
    code2 = compute_code(x2, y2)

    accept = False

    while True:

        # Case 1: Both points are inside
        if code1 == 0 and code2 == 0:
            accept = True
            break

        # Case 2: Both points are outside in the same region
        elif (code1 & code2) != 0:
            break

        # Case 3: Line is partially inside
        else:

            # Select the endpoint that is outside
            if code1 != 0:
                code_out = code1
            else:
                code_out = code2

            # Find intersection point
            if code_out & TOP:
                # Point is above clipping window
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax

            elif code_out & BOTTOM:
                # Point is below clipping window
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin

            elif code_out & RIGHT:
                # Point is to the right
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax

            elif code_out & LEFT:
                # Point is to the left
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            # Replace the outside endpoint
            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_code(x1, y1)

            else:
                x2, y2 = x, y
                code2 = compute_code(x2, y2)

    if accept:
        return x1, y1, x2, y2
    else:
        return None


# ---------------------------------------------------------
# Display Function
# ---------------------------------------------------------

def display():

    glClear(GL_COLOR_BUFFER_BIT)

    # -----------------------------------------
    # Draw clipping window
    # -----------------------------------------

    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2.0)

    glBegin(GL_LINE_LOOP)
    glVertex2f(xmin, ymin)
    glVertex2f(xmax, ymin)
    glVertex2f(xmax, ymax)
    glVertex2f(xmin, ymax)
    glEnd()

    # -----------------------------------------
    # Draw original line
    # -----------------------------------------
    
    glColor3f(1.0, 0.0, 0.0)
    glLineWidth(1.5)

    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

    # -----------------------------------------
    # Perform clipping
    # -----------------------------------------

    clipped_line = cohen_sutherland_clip(
        x1, y1, x2, y2
    )

    # -----------------------------------------
    # Draw clipped line
    # -----------------------------------------

    if clipped_line is not None:

        cx1, cy1, cx2, cy2 = clipped_line

        glColor3f(0.0, 1.0, 0.0)
        glLineWidth(4.0)

        glBegin(GL_LINES)
        glVertex2f(cx1, cy1)
        glVertex2f(cx2, cy2)
        glEnd()

    # -----------------------------------------
    # Display
    # -----------------------------------------

    glFlush()


# ---------------------------------------------------------
# Initialization
# ---------------------------------------------------------

def init():

    glClearColor(0.0, 0.0, 0.0, 1.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluOrtho2D(0, 800, 0, 600)

    glMatrixMode(GL_MODELVIEW)


# ---------------------------------------------------------
# Main Function
# ---------------------------------------------------------

def main():

    glutInit()

    glutInitDisplayMode(
        GLUT_SINGLE | GLUT_RGB
    )

    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)

    glutCreateWindow(
        b"Cohen-Sutherland Line Clipping"
    )

    init()

    glutDisplayFunc(display)

    glutMainLoop()


if __name__ == "__main__":
    main()