from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

angle = 0  # Rotation angle

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glEnable(GL_DEPTH_TEST)  # Enable depth testing

def display():
    global angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Move back to view the object
    glTranslatef(0.0, 0.0, -5)
    
    # Rotate the triangle
    glRotatef(angle, 0, 1, 0)  

    # Draw a triangle
    glBegin(GL_TRIANGLES)
    glColor3f(1, 0, 0)  # Red
    glVertex3f(-1, -1, 0)
    glColor3f(0, 1, 0)  # Green
    glVertex3f(1, -1, 0)
    glColor3f(0, 0, 1)  # Blue
    glVertex3f(0, 1, 0)
    glEnd()

    glutSwapBuffers()  # Swap buffers for smooth rendering
    angle += 1  # Increment rotation

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 1, 50)  # Perspective projection
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(500, 500)
    glutCreateWindow(b"OpenGL in Python")
    init()
    glutDisplayFunc(display)
    glutIdleFunc(display)  # Continuously update
    glutReshapeFunc(reshape)
    glutMainLoop()

if __name__ == "__main__":
    main()
