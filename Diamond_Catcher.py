from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

W_Width, W_Height = 500, 500
last_time = time.time()  #for the diamond_animation loop
last_time_key = time.time()  #for the key listener
start_time = time.time()   #for the catcher

diamond_x = random.randint(-W_Width // 2, W_Width // 2)
diamond_y = W_Height // 2
diamond_color = (
    random.uniform(0.3, 0.75), 
    random.uniform(0.3, 0.75), 
    random.uniform(0.3, 0.75)
)
diamond_size = 10
diamond_speed = 120
score = 0
game_over = False
paused = False

catcher_x = 0
catcher_width = 50
catcher_height = 10
catcher_y = -W_Height // 2 + 20
catcher_speed = 250

button_width, button_height = 20, 20
restart_button_pos = (-W_Width // 2 + 20, W_Height // 2 - 20)
play_pause_button_pos = (0, W_Height // 2 - 20)
terminate_button_pos = (W_Width // 2 - 20, W_Height // 2 - 20)

score = 0
game_over = False
paused = False
terminate_flag = False


def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx <= 0 and dy >= 0:
            return 3
        elif dx <= 0 and dy <= 0:
            return 4
        else:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx <= 0 and dy >= 0:
            return 2
        elif dx <= 0 and dy <= 0:
            return 5
        else:
            return 6
        
def convert_to_zone_zero(x, y, zone):
    if zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y
        
def convert_to_original_zone(x, y, zone):
    if zone == 0:
        return x,y
    if zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def draw_midpoint_line(x1, y1, x2, y2):
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    zone = find_zone(x1, y1, x2, y2)
    if zone != 0:
        x1, y1 = convert_to_zone_zero(x1, y1, zone)
        x2, y2 = convert_to_zone_zero(x2, y2, zone)
    dx = x2 - x1
    dy = y2 - y1
    d = (2 * dy) - dx
    dE = 2 * dy
    dNE = 2 * (dy - dx)
    
    x, y = x1, y1
    glBegin(GL_POINTS)
    while x <= x2:
        orig_x, orig_y = convert_to_original_zone(x, y, zone)
        glVertex2f(orig_x, orig_y)
        if d > 0:
            d += dNE
            y += 1
        else:
            d += dE
        x += 1
    glEnd()

def draw_catcher():
    if game_over:
        glColor3f(1, 0, 0)  #As the catcher should be red when game over
    else:
        glColor3f(1, 1, 1)
    x, y = catcher_x, -W_Height // 2 + 5
    draw_midpoint_line(x - 40, y, x + 40, y)
    draw_midpoint_line(x - 40, y, x - 60, y + 20)
    draw_midpoint_line(x + 40, y, x + 60, y + 20)
    draw_midpoint_line(x - 60, y + 20, x + 60, y + 20)



def draw_diamond():
    global diamond_x, diamond_y, diamond_color
    if game_over:
        return  #As there should not be any diamond when the game is over
    
    glColor3f(*diamond_color)
    draw_midpoint_line(diamond_x, diamond_y, diamond_x + diamond_size, diamond_y + diamond_size)
    draw_midpoint_line(diamond_x + diamond_size, diamond_y + diamond_size, diamond_x, diamond_y + 2 * diamond_size)
    draw_midpoint_line(diamond_x, diamond_y + 2 * diamond_size, diamond_x - diamond_size, diamond_y + diamond_size)
    draw_midpoint_line(diamond_x - diamond_size, diamond_y + diamond_size, diamond_x, diamond_y)




def check_collision():
    global catcher_x, catcher_y, catcher_width, catcher_height, diamond_x, diamond_y, diamond_size

    #catcher's boundaries
    catcher_left = catcher_x - 60  
    catcher_right = catcher_x + 60
    catcher_top = catcher_y + 20   
    catcher_bottom = catcher_y     


    #diamond's boundary
    diamond_left = diamond_x - diamond_size
    diamond_right = diamond_x + diamond_size
    diamond_bottom = diamond_y
    diamond_top = diamond_y + 2 * diamond_size

    #collision detection
    return (
        catcher_left < diamond_right and  
        catcher_right > diamond_left and  
        catcher_bottom < diamond_top and  
        catcher_top > diamond_bottom      
    )




def render_text(x, y, text, font):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    gluOrtho2D(-W_Width//2, W_Width//2, -W_Height//2, W_Height//2)
    draw_catcher()
    draw_diamond()
    draw_buttons()
    if game_over:
        glColor3f(1, 0, 0)
        render_text(-72, 0, "GAME OVER", GLUT_BITMAP_HELVETICA_18)
        render_text(-72, -30, f"Final Score: {score}", GLUT_BITMAP_HELVETICA_18)
    
    glutSwapBuffers()


def animate():
    global diamond_y, score, game_over, diamond_x, diamond_color, diamond_speed, last_time

    if not paused and not game_over:
        current_time = time.time()
        delta_time = current_time - last_time
        diamond_speed += 5 * delta_time  
        diamond_speed = min(diamond_speed, 400)

        last_time = current_time

        #diamond fall
        diamond_y -= diamond_speed * delta_time  

        if check_collision():
            score += 1
            print(f"Score: {score}")
            diamond_speed = 150 * (1 + score * 0.15)  
            diamond_speed = min(diamond_speed, 400)

            diamond_y = W_Height // 2
            diamond_x = random.randint(-W_Width // 2 + diamond_size, W_Width // 2 - diamond_size)

            diamond_color = (
    random.uniform(0.4, 0.75), 
    random.uniform(0.4, 0.75), 
    random.uniform(0.4, 0.75)
)

            
        elif diamond_y < -W_Height // 2:
            game_over = True
            print(f"Game Over. Final Score: {score}")
    glutPostRedisplay()



def specialKeyListener(key, x, y):
    global catcher_x, last_time_key, game_over

    if game_over:
        return

    current_time = time.time()
    delta_time = min(current_time - last_time_key, 0.05) 
    last_time_key = current_time
    catcher_speed = diamond_speed * 0.85  


    movement = catcher_speed * delta_time

    if key == GLUT_KEY_LEFT:
        catcher_x = max(-W_Width // 2 + 60, catcher_x - movement)
    elif key == GLUT_KEY_RIGHT:
        catcher_x = min(W_Width // 2 - 60, catcher_x + movement)

    glutPostRedisplay()





def restart_game():
    global diamond_x, diamond_y, diamond_speed, score, game_over, paused, catcher_x, last_time, diamond_color
    
    print("Starting Over")
    diamond_x = random.randint(-W_Width // 2 + diamond_size, W_Width // 2 - diamond_size)
    diamond_y = W_Height // 2
    diamond_speed = 120 
    score = 0
    game_over = False
    paused = False
    catcher_x = 0
    last_time = time.time()  #Reset delta timer
    diamond_color = (
        random.uniform(0.4, 0.75),
        random.uniform(0.4, 0.75),
        random.uniform(0.4, 0.75)
    )


def toggle_pause():
    global paused
    paused = not paused


def terminate_game():
    print(f"Goodbye. Final Score: {score}")
    glutLeaveMainLoop()


def mouse_listener(button, state, x, y):
    global paused, game_over
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        gl_x = x - W_Width // 2
        gl_y = (W_Height // 2 - y)
        
        if is_within_button(gl_x, gl_y, (-W_Width // 2 + 20, W_Height // 2 - 20)):
            restart_game()
        elif is_within_button(gl_x, gl_y, (0, W_Height // 2 - 20)):
            if not game_over:
                toggle_pause()
        elif is_within_button(gl_x, gl_y, (W_Width // 2 - 20, W_Height // 2 - 20)):
            terminate_game()
        
        glutPostRedisplay()

def draw_buttons():
    glColor3f(0.1, 0.6, 1)
    x, y = restart_button_pos
    draw_restart_symbol(x, y)

    glColor3f(1, 0.6, 0)
    x, y = play_pause_button_pos
    if paused:
        draw_play_symbol(x, y)
    else:
        draw_pause_symbol(x, y)

    glColor3f(1, 0, 0)
    x, y = terminate_button_pos
    draw_terminate_symbol(x, y)


def draw_play_symbol(x, y):
    size = 9
    draw_midpoint_line(x - size, y - size, x + size, y)
    draw_midpoint_line(x + size, y, x - size, y + size)
    draw_midpoint_line(x - size, y + size, x - size, y - size)

def draw_pause_symbol(x, y):
    bar_width = 6
    bar_height = 8

    draw_midpoint_line(x - bar_width, y - bar_height, x - bar_width, y + bar_height)
    draw_midpoint_line(x - bar_width + 1, y - bar_height, x - bar_width + 1, y + bar_height)
    
    draw_midpoint_line(x + bar_width, y - bar_height, x + bar_width, y + bar_height)
    draw_midpoint_line(x + bar_width - 1, y - bar_height, x + bar_width - 1, y + bar_height)

def draw_restart_symbol(x, y):
    size = 12
    draw_midpoint_line(x + size, y, x - size, y)
    
    draw_midpoint_line(x - size, y, x - size + 5, y + 5)
    draw_midpoint_line(x - size, y, x - size + 5, y - 5)

def draw_terminate_symbol(x, y):
    size = 8

    draw_midpoint_line(x - size, y - size, x + size, y + size)
    draw_midpoint_line(x - size, y + size, x + size, y - size)


def is_within_button(x, y, button_pos):
    bx, by = button_pos
    return (
        bx - button_width // 2 <= x <= bx + button_width // 2 and
        by - button_height // 2 <= y <= by + button_height // 2
    )



def init():
    glClearColor(0, 0, 0, 1)

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(100, 100)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Catch the Diamonds")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouse_listener)
glutMainLoop()



