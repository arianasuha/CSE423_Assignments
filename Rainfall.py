#task1
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random

W_Width, W_Height = 500, 500

rain = []
rain_speed = 1.5
rain_direction = 0
background = 0    #controls the background color


def drawShapes():
    
    # Roof
    glBegin(GL_TRIANGLES)
    glColor3f(0.40, 0, 0)
    glVertex2f(-100, 0)
    glVertex2f(0, 100)
    glVertex2f(100, 0)
    glEnd()
    
    # Walls
    glBegin(GL_TRIANGLES)
    glColor3f(0, 0.7, 0.4)
    glVertex2f(-80, 0)
    glVertex2f(80, 0)
    glVertex2f(-80, -100)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0, 0.5, 0.5)
    glVertex2f(80, 0)
    glVertex2f(80, -100)
    glVertex2f(-80, -100)
    glEnd()
    
    # Doors
    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.2, 0)
    glVertex2f(-25, -100)
    glVertex2f(25, -100)
    glVertex2f(-25, -30)
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0, 0.1)
    glVertex2f(25, -100)
    glVertex2f(25, -30)
    glVertex2f(-25, -30)
    glEnd()
    
    # Windows
    # Right Window
    glBegin(GL_TRIANGLES)
    glColor3f(0.95, 0.75, 0.75)
    glVertex2f(40, -60)
    glVertex2f(70, -60)
    glVertex2f(40, -30)
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3f(0.95, 0.75, 0.75)
    glVertex2f(70, -30)
    glVertex2f(70, -60)
    glVertex2f(40, -30)
    glEnd()

    # Left Window
    glBegin(GL_TRIANGLES)
    glColor3f(0.95, 0.75, 0.75)
    glVertex2f(-70, -60)
    glVertex2f(-40, -60)
    glVertex2f(-70, -30)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.95, 0.75, 0.75)
    glVertex2f(-40, -30)
    glVertex2f(-40, -60)
    glVertex2f(-70, -30)
    glEnd()

    
    # Base Line 
    glLineWidth(10)
    glBegin(GL_LINES)
    glColor3f(0.40, 0, 0)
    glVertex2f(-95, -105)
    glVertex2f(95, -105)
    glEnd()
    glLineWidth(1)


    # Door knob
    glPointSize(6)
    glBegin(GL_POINTS)
    glColor3f(0, 0, 0)
    glVertex2f(15, -75)
    glEnd()

    # Right Window Cross 
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(40, -45)
    glVertex2f(70, -45)
    glVertex2f(55, -30)
    glVertex2f(55, -60)
    glEnd()

    # Left Window Cross
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 0.0)

    # Horizontal line
    glVertex2f(-70, -45)  
    glVertex2f(-40, -45)

    # Vertical line
    glVertex2f(-55, -30)  
    glVertex2f(-55, -60)

    glEnd()


def rain_initialize():  #Initializes 120 raindrops at random positions within the window.
    global rain
    
    for i in range(120): 
        x = random.randint(-W_Width // 2, W_Width // 2)  
        y = random.randint(-W_Height // 2, W_Height // 2) 
        rain.append([x, y])  

# X values range from -250 to 250 (so rain covers the full width).
# Y values range from -250 to 250 (so rain covers the full height).

def Rainfall():
    global rain, rain_direction, rain_speed, background
    if background < 0.5:
        glColor3f(0.3, 0.5, 0.6)   #light blue rain
    else:
        glColor3f(0.0, 0.0, 0.7)   #screen is light
        
    glBegin(GL_LINES)
    for iter in rain:
        x, y = iter
        glVertex2f(x, y)   #starting point of the raindrop
        glVertex2f(x + rain_direction * 5, y - 10)    #ending point of the rain drop
    glEnd()

    # If rain_direction = 0 → No sideways movement.
    # If rain_direction > 0 → Rain goes right.
    # If rain_direction < 0 → Rain goes left.



def keyboardListener(key, x, y):
    global background
    if key == b'd':
        background = min(1, background + 0.1) 
    if key == b'n':
        background = max(0, background - 0.1)
    glutPostRedisplay()   


def specialKeyListener(key, x, y):   
    global rain_direction
    if key == GLUT_KEY_LEFT:
        rain_direction = max(-1, rain_direction - 0.1)   #so the rain doesn’t move too far left.
    if key == GLUT_KEY_RIGHT:
        rain_direction = min(1, rain_direction + 0.1)
    glutPostRedisplay()


def display():
    global background
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(background, background, background, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    drawShapes()
    Rainfall()

    glutSwapBuffers()


def animate():
    global rain, rain_direction, rain_speed, background       
    for drop in rain:
        drop[0] += rain_direction  # Move horizontally based on direction
        drop[1] -= rain_speed      # Move downward by rain_speed

    new_rain = []  # Create a new list to store valid raindrops

    for drop in rain:
        if drop[1] > -W_Height // 2:  # Keep only raindrops above the bottom limit
            new_rain.append(drop)

    rain = new_rain  # Update the rain list with only valid raindrops


    while len(rain) < 120:  
        new_x = random.randint(-W_Width, W_Width)
        new_y = random.randint((W_Height // 2) + 5, (W_Height // 2) + 10)
        rain.append([new_x, new_y])
    glutPostRedisplay()


def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)
    rain_initialize()


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

glutCreateWindow(b"House in Rainfall")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)

glutMainLoop()