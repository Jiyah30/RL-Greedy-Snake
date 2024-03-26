import numpy as np

import pygame
import gym
from gym import spaces

from utils.snake import Snake
from utils.food import Food
from utils.utils import init_board, Color, accelerate, show_score

class GreedySnakeEnv(gym.Env):
    
    def __init__(self, args):
        
        super().__init__()
        
        self.args = args
        self.setting_dict, self.snake_dict, self.food_dict = init_board(self.args)
        
        # setting
        self.window = self.setting_dict["window"]
        self.fps = self.setting_dict["fps"]
        self.speed = self.setting_dict["speed"]
        self.speed_up = self.setting_dict["speed_up"]
        self.score = self.setting_dict["score"]

        # snake
        self.snake_position = self.snake_dict["snake_position"]
        self.snake_body = self.snake_dict["snake_body"]
        self.direction = self.snake_dict["direction"]
        self.change_to = self.snake_dict["change_to"]

        # food
        self.food_position = self.food_dict["food_position"]
        self.poison_food = self.food_dict["poison_food"]
        self.food_spawn = self.food_dict["food_spawn"]

        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low = 0, high = 255, shape = (int(self.args.window_size_x/10), int(self.args.window_size_y/10), 3), dtype = np.uint8)
        
        # l1 dist
        # x, y = self.snake_position[0], self.snake_position[1]
        # self.prevD = [abs(x - self.food_position[0]), abs(y - self.food_position[1])]
        self.prevD = [-10, -10]

        self.observation = np.zeros((int(self.args.window_size_x/10), int(self.args.window_size_y/10), 3), dtype = np.uint8)

    def snake2vec(self, snake_body, food_position, poison_food):
        observation = np.zeros((int(self.args.window_size_x/10), int(self.args.window_size_y/10), 3), dtype = np.uint8)
        for coordinate in snake_body:
            x, y = int(coordinate[0]/10), int(coordinate[1]/10)
            # print(f"snake_body: x = {x}, y = {y}")
            observation[x-1, y-1, 0] = 1

        x, y = int(food_position[0]/10), int(food_position[1]/10)
        # print(f"food_position: x = {x}, y = {y}")
        observation[x-1, y-1, 1] = 1
        
        x, y = int(poison_food[0]/10), int(poison_food[1]/10)
        # print(f"poison_food: x = {x}, y = {y}")
        observation[x-1, y-1, 2] = 1

        return observation
        

    def step(self, action):
        
        if action == 0:
            self.change_to = 'UP'
        elif action == 1:
            self.change_to = 'DOWN'
        elif action == 2:
            self.change_to = 'LEFT'
        elif action == 3:
            self.change_to = 'RIGHT'

        # food
        self.food = Food(self.args)
        self.food_position, self.food_spawn, self.poison_food = self.food.spawning(self.food_spawn, self.food_position, self.poison_food)

        # snake
        self.snake = Snake()
        self.direction = self.snake.check_direction(self.direction, self.change_to)
        self.snake_position = self.snake.moving(self.direction, self.snake_position)
        self.snake_body, self.score, self.food_spawn, self.speed_up, reward = self.snake.growing(self.snake_body, self.snake_position, self.food_position, self.food_spawn, self.score)

        self.speed, self.speed_up = accelerate(self.speed, self.speed_up)
        self.fps.tick(self.speed)

        obs = self.snake2vec(self.snake_body, self.food_position, self.poison_food)
        done = self.is_done

        if done:
            reward -= 1.5

        # x, y = self.snake_position[0], self.snake_position[1]
        # dx, dy = x - self.food_position[0], y - self.food_position[1]
        # px, py = self.prevD[0], self.prevD[1]
        sum_d, sum_p = self.calcDist(self.snake_position, self.food_position)
        if sum_d < sum_p:
            reward += 0.1
        else:
            reward -= 0.3
        
        return obs, reward, done, {}

    def calcDist(self, src, dst):
        x, y = src[0], src[1]
        dx, dy = abs(x - dst[0]), abs(y - dst[1])
        px, py = self.prevD[0], self.prevD[1]
        sum_d = dx + dy
        sum_p = px + py
        self.prevD = [dx, dy]
        # print(sum_d, sum_p)

        return sum_d, sum_p

    @property
    def is_done(self):
        done = False

        # game over
        if self.snake_position[0] < 0 or self.snake_position[0] > (self.args.window_size_x - 10):
            done = True
        elif self.snake_position[1] < 0 or self.snake_position[1] > (self.args.window_size_y - 10):
            done = True
        elif self.snake_position[0] == self.poison_food[0] and self.snake_position[1] == self.poison_food[1]:
            done = True
        for block in self.snake_body[1:]:
            if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                done = True
        
        return done

    def reset(self):

        restart = False

        # game over
        if self.snake_position[0] < 0 or self.snake_position[0] > (self.args.window_size_x - 10):
            restart = True
        elif self.snake_position[1] < 0 or self.snake_position[1] > (self.args.window_size_y - 10):
            restart = True
        elif self.snake_position[0] == self.poison_food[0] and self.snake_position[1] == self.poison_food[1]:
            restart = True
        for block in self.snake_body[1:]:
            if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                restart = True

        if restart:
            
            self.setting_dict, self.snake_dict, self.food_dict = init_board(self.args)
            
            # setting
            self.window = self.setting_dict["window"]
            self.fps = self.setting_dict["fps"]
            self.speed = self.setting_dict["speed"]
            self.speed_up = self.setting_dict["speed_up"]
            self.score = self.setting_dict["score"]

            # snake
            self.snake_position = self.snake_dict["snake_position"]
            self.snake_body = self.snake_dict["snake_body"]
            self.direction = self.snake_dict["direction"]
            self.change_to = self.snake_dict["change_to"]

            # food
            self.food_position = self.food_dict["food_position"]
            self.poison_food = self.food_dict["poison_food"]
            self.food_spawn = self.food_dict["food_spawn"]

            # l1 list
            _, _ = self.calcDist(self.snake_position, self.food_position)

        obs = np.zeros((int(self.args.window_size_x/10), int(self.args.window_size_y/10), 3), dtype = np.uint8)
        
        return obs

    def render(self, mode = "human"):
        
        self.window.fill(Color.black)
        
        # draw snake
        for pos in self.snake_body:
            # pygame.draw.rect(window, color, coordinates of x and y)
            # coordinates of x and y -> pygame.Rect(x, y, size_x, size_y)
            pygame.draw.rect(self.window, Color.green, pygame.Rect(pos[0], pos[1], 10, 10))

        # draw food
        pygame.draw.rect(self.window, Color.white, pygame.Rect(self.food_position[0], self.food_position[1], 10, 10))
        pygame.draw.rect(self.window, Color.red, pygame.Rect(self.poison_food[0], self.poison_food[1], 10, 10))

        # show score
        show_score(Color.white, 'consolas', 20, self.score, self.window)

        pygame.display.update()