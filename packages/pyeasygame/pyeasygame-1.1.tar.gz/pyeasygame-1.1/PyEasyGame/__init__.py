import pygame
import random as r
import keyboard as kb
import sys
import time as t
pygame.init()

rect = []
clock = pygame.time.Clock()
pygame.display.set_caption('PyEasy Game Window')

last_time = t.time()

time = 8
frames = 60
screens = []
screen_sizes = []

def collide(rect1, rect2, mouse_boolean, mouse_x, mouse_y):
    if len(rect) >= 1:
        if not mouse_boolean:
            if 'playerx' not in rect1 and 'playery' not in rect1:
                if pygame.Rect(rect1).colliderect(pygame.Rect(rect2)):
                    return True
            if 'playerx' in rect1 and 'playery' in rect1:
                if rect[0].colliderect(pygame.Rect(rect2)):
                    return True
        if mouse_boolean:
            if 'playerx' not in rect1 and 'playery' not in rect1:
                if pygame.Rect(rect1).collidepoint((mouse_x, mouse_y)):
                    return True
            if 'playerx' in rect1 and 'playery' in rect1:
                if rect[0].collidepoint((mouse_x, mouse_y)):
                    return True
    pass

drawimg = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
button_click = ''

def button(image, x,y,click, draw_button):
    mouse = pygame.mouse.get_pressed()
    mx,my = pygame.mouse.get_pos()
    if draw_button:
        screens[0].blit(image, (x,y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if len(screens) >= 1:
                if click == 'left':
                    if pygame.Rect(x,y,image.get_width(),image.get_height()).collidepoint((mx,my)):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            click = 'down'
                        if event.type == pygame.MOUSEBUTTONUP:
                            click = 'up'
                        if click == 'up':
                            return True
                if click == 'right':
                    if pygame.Rect(x,y,image.get_width(),image.get_height()).collidepoint((mx,my)):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            click = 'down'
                        if event.type == pygame.MOUSEBUTTONUP:
                            click = 'up'
                        if click == 'up':
                            return True
    pass

def pickup_item(image,x,y,condition,number):
    mx,my = pygame.mouse.get_pos()
    mouse = pygame.mouse.get_pressed()
    if drawimg[number - 1]:
        screens[0].blit(image, (x,y))
        if condition == 'Player' or 'player' or 'PLAYER':
            if pygame.Rect(x,y,image.get_width(), image.get_height()).colliderect(rect[0]):
                drawimg[number - 1] = False
                return True 
        if condition == 'Mouse' or 'mouse' or 'MOUSE':
            if pygame.Rect(x,y,image.get_width(),image.get_height()).collidepoint((mx,my)):
                if mouse[0]:
                    drawimg[number - 1] = False
                    return True
pass

def player_pos(xy,change_xy,value):
    if xy != '':
        if not change_xy:
            if xy == 'x':
                return rect[0].x
            if xy == 'y':
                return rect[0].y
        if change_xy:
            if xy == 'x':
                rect[0].x = value
            if xy == 'y':
                rect[0].y = value
    if rect[0].x < 0:
        rect[0].x = 0
    if rect[0].x + rect[0].width > screen_sizes[0]:
        rect[0].x = screen_sizes[0] - rect[0].width
    if rect[0].y < 0:
        rect[0].y = 0
    if rect[0].y + rect[0].height > screen_sizes[1]:
        rect[0].y = screen_sizes[1] - rect[0].height
    pass

def insert_text(text,font,color,x,y,show_text, variable_boolean, variable):
    if variable_boolean == False:
        screens[0].blit(font.render(text, show_text, color), (x,y))
    if variable_boolean:
        screens[0].blit(font.render(text + str(variable), show_text, color), (x,y))
    pass

run_once = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]

def timer(start, stop_time, timer_value):
    global start_ticks
    if run_once[timer_value - 1]:
        start_ticks = pygame.time.get_ticks()
        run_once[timer_value - 1] = False
    if start == True:
        timerTime = float((pygame.time.get_ticks()-start_ticks)/1000)
        if timerTime >= stop_time:
            timerTime = stop_time
        return timerTime
    pass
 
def create_screen(width, height, fullscreen, resizable):
    if len(screens) < 1:
        if not fullscreen:
            screen = pygame.display.set_mode((width,height))
            screens.append(screen)
            screen_sizes.append(width)
            screen_sizes.append(height)
        if not resizable:
            screen = pygame.display.set_mode((width,height))
            screens.append(screen)
            screen_sizes.append(width)
            screen_sizes.append(height)
        if fullscreen:
            screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
            screens.append(screen)
            screen_sizes.append(width)
            screen_sizes.append(height)
        if resizable:
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            screens.append(screen)
            screen_sizes.append(width)
            screen_sizes.append(height)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pass

# def collision_box(image,x,y,collision):
#     col_box = pygame.Rect(x,y,image.get_width(), image.get_height())
#     if collision:
#         if rect[0].colliderect(pygame.Rect(x,y,image.get_width(),image.get_height())):
#             if abs(rect[0].right - col_box.left) < 15:
#                 rect[0].x = x - rect[0].height
#             if abs(rect[0].bottom - col_box.top) < 15:
#                 rect[0].y = y - rect[0].height
#             if abs(rect[0].left - col_box.right) < 15:
#                 rect[0].x = x + image.get_width()
#             if abs(rect[0].top - col_box.bottom) < 15:
#                 rect[0].y = y + image.get_height()
#         pass
#     screens[0].blit(image, (x,y))
    pass

def fill_screen(red,green,blue):
    if len(screens) >= 1:
        screens[0].fill((red,green,blue))
    pass

def set_name(name):
    pygame.display.set_caption(name)
    pass

def set_icon(image):
    pygame.display.set_icon(image)
    pass

def draw_image(image, xy, draw_img):
    if draw_img:
        if len(screens) >= 1:
            screens[0].blit(image, xy)
    pass

def set_fps(fps):
    global frames
    frames = fps
    return clock.get_fps()
    pass

def draw_rect(x,y,width,height,color, radius_boolean, radius_value,draw_rect):
    if draw_rect:
        if len(screens) >= 1:
            if radius_boolean == False:
                pygame.draw.rect(screens[0], color, (x,y,width,height))
            else:
                pygame.draw.rect(screens[0], color, (x,y,width,height), radius_value)
    pass

def resize(image, new_width, new_height):
    return pygame.transform.scale(image, (new_width, new_height))
    pass

player_width = 0
player_height = 0
jumped = False
jump_velocity = 20

def player(image,x,y,move_left,move_right,move_up,move_down,jump,speed, collide_sides, sticky_keys):
    image_player = None
    run_once = True
    global jump_velocity, jumped, time, last_time
    dt = t.time() - last_time
    dt *= frames
    last_time = t.time()
    if len(screens) >= 1:
        player_width = image.get_width()
        player_height = image.get_height()
        if run_once:
            rect.append(pygame.Rect(x,y,image.get_width(),image.get_height()))
            run_once = False
        image_player = image
        if jump != '':
            if jumped == False and kb.is_pressed(jump):
                jumped = True
        if sticky_keys:
            if collide_sides == False:
                if move_left != '':
                    if kb.is_pressed(move_left):
                        rect[0].x -= speed * dt
                if move_right != '':
                    if kb.is_pressed(move_right):
                        rect[0].x += speed * dt 
                if move_up != '':
                    if kb.is_pressed(move_up):
                        rect[0].y -= speed * dt
                if move_down != '':
                    if kb.is_pressed(move_down):
                        rect[0].y += speed * dt
                if jump != '':
                    if jumped:
                        rect[0].y -= jump_velocity
                        jump_velocity -= 1
                        if jump_velocity < - 20:
                            jumped = False
                            jump_velocity = 20
            if collide_sides == True:
                if move_left != '':
                    if kb.is_pressed(move_left) and rect[0].x >= 0:
                        rect[0].x -= speed * dt
                if move_right != '':
                    if kb.is_pressed(move_right) and rect[0].x <= screen_sizes[0] - player_width:
                        rect[0].x += speed * dt 
                if move_up != '':
                    if kb.is_pressed(move_up) and rect[0].y >= 0:
                        rect[0].y -= speed * dt
                if move_down != '':
                    if kb.is_pressed(move_down) and rect[0].y <= screen_sizes[1] - player_height:
                        rect[0].y += speed * dt
                if jump != '':
                    if jumped:
                        rect[0].y -= jump_velocity
                        jump_velocity -= 1
                        if jump_velocity < - 20:
                            jumped = False
                            jump_velocity = 20
                if rect[0].x < 0:
                    rect[0].x = 0
                if rect[0].x + rect[0].width > screen_sizes[0]:
                    rect[0].x = screen_sizes[0] - rect[0].width
                if rect[0].y < 0:
                    rect[0].y = 0
                if rect[0].y + rect[0].height > screen_sizes[1]:
                    rect[0].y = screen_sizes[1] - rect[0].height
        if not sticky_keys:
            if move_left != '':
                if kb.is_pressed(move_left):
                    rect[0].x -= speed * dt
            elif move_right != '':
                if kb.is_pressed(move_right):
                    rect[0].x += speed * dt 
            elif move_up != '':
                if kb.is_pressed(move_up):
                    rect[0].y -= speed * dt
            elif move_down != '':
                if kb.is_pressed(move_down):
                    rect[0].y += speed * dt
            elif jump != '':
                if jumped:
                    rect[0].y -= jump_velocity
                    jump_velocity -= 1
                    if jump_velocity < - 20:
                        jumped = False
                        jump_velocity = 20
        if collide_sides == True:
            if move_left != '':
                if kb.is_pressed(move_left) and rect[0].x >= 0:
                    rect[0].x -= speed * dt
            elif move_right != '':
                if kb.is_pressed(move_right) and rect[0].x <= screen_sizes[0] - player_width:
                    rect[0].x += speed * dt 
            elif move_up != '':
                if kb.is_pressed(move_up) and rect[0].y >= 0:
                    rect[0].y -= speed * dt
            elif move_down != '':
                if kb.is_pressed(move_down) and rect[0].y <= screen_sizes[1] - player_height:
                    rect[0].y += speed * dt
            elif jump != '':
                if jumped:
                    rect[0].y -= jump_velocity
                    jump_velocity -= 1
                    if jump_velocity < - 20:
                        jumped = False
                        jump_velocity = 20
            if rect[0].x < 0:
                rect[0].x = 0
            if rect[0].x + rect[0].width > screen_sizes[0]:
                rect[0].x = screen_sizes[0] - rect[0].width
            if rect[0].y < 0:
                rect[0].y = 0
            if rect[0].y + rect[0].height > screen_sizes[1]:
                rect[0].y = screen_sizes[1] - rect[0].height
        screens[0].blit(image_player, rect[0])
        pygame.time.delay(time)
    pass

def load_img(img_location):
    return pygame.image.load(img_location)
    pass

def lives(lives_image1, lives_image2, x,y,lives_amount,lives_amount2, draw_lives):
    if len(screens) >= 1:
        if draw_lives:
            for i in range(lives_amount2):
                screens[0].blit(lives_image2,(x + lives_image2.get_width() * i ,y))
            for i in range(lives_amount):
                screens[0].blit(lives_image1, (x + lives_image1.get_width() * i,y))
    # if len(screens) >= 1:
    #     if draw_lives:
    #         for i in range(lives_amount2):
    #             if i < lives_amount:
    #                 screens[0].blit(lives_image1,(x + lives_image1.get_width() * i,y,lives_image1.get_width(),lives_image1.get_height()))
    #             else:
    #                 screens[0].blit(lives_image2,(x + lives_image2.get_width() * i,y,lives_image2.get_width(),lives_image2.get_height()))
    if lives_amount <= 0:
        lives_amount = 0
    return lives_amount
    pass

def delay_time(time_delay):
    global time
    time = time_delay
    pass

def rotate_img(image, angle):
    return pygame.transform.rotate(image, angle)

def update_screen():
    global frames
    clock.tick(frames)
    pygame.display.flip()
    pass

def key_pressed(key):
    if kb.is_pressed(key):
        return True
    pass

def render_font(font, size):
    return pygame.font.SysFont(font, size)
    pass

def mouse_pos(xy):
    mx,my = pygame.mouse.get_pos()
    if xy == 'x':
        return mx
    if xy == 'y':
        return my
    pass

def mouse_click(click):
    mouse = pygame.mouse.get_pressed()
    if click == 'left':
        if mouse[0] == True:
            return 'down'
        if mouse[0] == False:
            return 'up'
    if click == 'right':
        if mouse[2] == True:
            return 'down'
        if mouse[2] == False:
            return 'up'
    pass