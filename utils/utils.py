import pygame
import random

# colors
class Color():

    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)

# initial board
def init_board(args):

    # game settings
    pygame.init()
    pygame.display.set_caption('Greedy Snake')
    window = pygame.display.set_mode((args.window_size_x, args.window_size_y))
    fps = pygame.time.Clock()
    speed = args.speed
    speed_up = 0
    score = 0

    setting_dict = {"window": window, 
                    "fps": fps, 
                    "speed": speed,
                    "speed_up": speed_up, 
                    "score": score}

    # snake
    snake_position = [int(args.window_size_x / 2), int(args.window_size_y / 2)]
    snake_body = [[int(args.window_size_x / 2), int(args.window_size_y / 2)], 
                  [int(args.window_size_x / 2) - 10, int(args.window_size_y / 2)], 
                  [int(args.window_size_x / 2) - 20, int(args.window_size_y / 2)]]
    direction = 'RIGHT'
    change_to = direction

    snake_dict = {"snake_position": snake_position, 
                  "snake_body": snake_body, 
                  "direction": direction, 
                  "change_to": change_to}

    # food
    food_position = [random.randrange(1, (args.window_size_x // 10)) * 10, random.randrange(1, (args.window_size_y // 10)) * 10]
    poison_food = [random.randrange(1, (args.window_size_x // 10)) * 10, random.randrange(1, (args.window_size_y // 10)) * 10]
    while poison_food == food_position:
        poison_food = [random.randrange(1, (args.window_size_x // 10)) * 10, random.randrange(1, (args.window_size_y // 10)) * 10]
    food_spawn = True

    food_dict = {"food_position": food_position, 
                 "poison_food": poison_food, 
                 "food_spawn": food_spawn}

    return setting_dict, snake_dict, food_dict

# accelerate
def accelerate(speed, speed_up):
    if speed <= 30 and speed_up == 1 :
        speed += 1
        speed_up = 0
    
    return speed, speed_up

# show score
def show_score(color, font, size, score, window):

    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    window.blit(score_surface, score_rect)

# restart
def restart(color, font, size, window, args):
    restart_font = pygame.font.SysFont(font, size)
    restart_surface = restart_font.render('Press UP to restart', True, color)
    restart_rect = restart_surface.get_rect()
    restart_rect.midtop = (args.window_size_x / 2, args.window_size_y / 1.4)
    window.blit(restart_surface, restart_rect)