#task2

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import random

W_Width, W_Height = 500, 500
box_size = 220

points = []
point_speed = 0.3
point_radius = 6
blink, frozen = False, False

class point:
    def __init__(self, x, y, new_x, new_y, col):
        self.x = x
        self.y = y
        self.new_x = new_x
        self.new_y = new_y
        self.color = col
        self.visible = True


def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width / 2)
    b = (W_Height / 2) - y
    return a, b


def draw_points(x, y, radius, color):
    glColor3f(*color)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for angle in range(0, 361, 5):
        radian = math.radians(angle)
        glVertex2f(x + radius * math.cos(radian), y + radius * math.sin(radian))
    glEnd()


def draw_amazing_box():
    glLineWidth(4)
    glColor3f(1.0, 1.0, 1.0)   #color of the box
    glBegin(GL_LINE_LOOP)
    glVertex2f(-box_size, box_size)   #four corners of the square box
    glVertex2f(-box_size, -box_size)
    glVertex2f(box_size, -box_size)
    glVertex2f(box_size, box_size)
    glEnd()

def keyboardListener(key, x, y):
    global frozen
    if key == b' ':
        frozen = not frozen
        state = "Frozen" if frozen else "Unfrozen"
        print(f"{frozen}: {state}")
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global point_speed
    if key == GLUT_KEY_UP:
        point_speed *= 1.2
        for point in points:
            point.new_x = (point.new_x / abs(point.new_x)) * point_speed
            point.new_y = (point.new_y / abs(point.new_y)) * point_speed
        print("Speed Increased")
    elif key == GLUT_KEY_DOWN:
        point_speed /= 1.2
        for point in points:
            point.new_x = (point.new_x / abs(point.new_x)) * point_speed
            point.new_y = (point.new_y / abs(point.new_y)) * point_speed
        print("Speed Decreased")
    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global blink
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        blink = not blink
        print("Blinking", "ON" if blink else "OFF")
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        converted_x, converted_y = convert_coordinate(x, y)
        changed_x, changed_y = random.choice([-1, 1]) * point_speed, random.choice([-1, 1]) * point_speed
        color = (random.random(), random.random(), random.random())
        points.append(point(converted_x, converted_y, changed_x, changed_y, color)) 
    glutPostRedisplay()
    

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    for point in points:
        if point.visible or not blink:
            draw_points(point.x, point.y, point_radius, point.color)
    draw_amazing_box()
    
    glutSwapBuffers()


def animate():
    global frozen
    if frozen == True:
        return
    
    for point in points:
        point.x += point.new_x
        point.y += point.new_y
        

        #boundary check for x
        if point.x + point_radius > box_size:
            point.x = box_size - point_radius
            point.new_x = - point.new_x
        elif point.x - point_radius < -box_size:
            point.x = -box_size + point_radius
            point.new_x = - point.new_x
        
        #boundary check for y
        if point.y + point_radius > box_size:
            point.y = box_size - point_radius
            point.new_y = - point.new_y
        elif point.y - point_radius < -box_size:
            point.y = -box_size + point_radius
            point.new_y = - point.new_y

        if blink == True:
            point.visible = not point.visible

    glutPostRedisplay()


def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b"Amazing Box with Points")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()

