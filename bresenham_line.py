from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

points = []

def bresenham_line(x1,y1,x2,y2):
    x,y=x1,y1
    diffx=abs(x2-x1)
    diffy=abs(y2-y1)
    
    # print(diffx,diffy)
    points.clear()
    points.append((x,y))

    slope=diffy/diffx
    if 0<=slope<=1:
        p=[0]*(diffx+1)
        para1=2*diffy
        para2=2*diffy-2*diffx
        p[0]=para1-diffx


        for i in range(0,diffx):
            if p[i]<0:
                x=x+1
                p[i+1]=p[i]+para1
            else:
                x,y=x+1,y+1
                p[i+1]=p[i]+para2  
            points.append((x,y))  
    if slope>1:
            p=[0]*(diffy+1)
            para1=2*diffx
            para2=2*diffx-2*diffy
            p[0]=para1-diffy
    
    
            for i in range(0,diffy):
                if p[i]<0:
                    y=y+1
                    p[i+1]=p[i]+para1
                else:
                    x,y=x+1,y+1
                    p[i+1]=p[i]+para2 
                points.append((x,y))  
    # return points

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 1.0, 0.0)
    glPointSize(5)
    glBegin(GL_POINTS)
    for x, y in points:
        glVertex2f(x, y)
    glEnd()
    glFlush()

def init():

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    # gluOrtho2D(0, 100, 0, 100)


# bresenham_line(20, 10, 30, 18)
bresenham_line(100, 100,700, 500)

glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)

glutInitWindowSize(800, 600)
glutInitWindowPosition(100, 100)

glutCreateWindow(b"Bresenham Line Algorithm")

init()

glutDisplayFunc(display)

glutMainLoop()

# p1=bresenham_line(20,10,30,18)
# print("example 1",p1) 
# p2=bresenham_line(2,2,5,9)      
# print("example 2",p2)