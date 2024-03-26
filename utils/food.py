import random

class Food():

    def __init__(self, args):
        
        self.window_size_x = args.window_size_x
        self.window_size_y = args.window_size_y

    def spawning(self, food_spawn, food_position, poison_food):

        if not food_spawn:
            food_position = [random.randrange(1, (self.window_size_x // 10)) * 10, random.randrange(1, (self.window_size_y // 10)) * 10]
            poison_food = [random.randrange(1, (self.window_size_x // 10)) * 10, random.randrange(1, (self.window_size_y // 10)) * 10]
            while poison_food == food_position:
                poison_food = [random.randrange(1, (self.window_size_x // 10)) * 10, random.randrange(1, (self.window_size_y // 10)) * 10]
        food_spawn = True

        return food_position, food_spawn, poison_food