class Snake():

    def __init__(self):
        pass

    def check_direction(self, direction, change_to):

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        return direction

    def moving(self, direction, snake_position):
        
        if direction == 'UP':
           snake_position[1] -= 10
        if direction == 'DOWN':
           snake_position[1] += 10
        if direction == 'LEFT':
           snake_position[0] -= 10
        if direction == 'RIGHT':
           snake_position[0] += 10

        return snake_position

    def growing(self, snake_body, snake_position, food_position, food_spawn, score):
        
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
           score += 1
           speed_up = 1
           food_spawn = False
           reward = 1.0
        else:
           speed_up = 0
           snake_body.pop()
           reward = 0.0

        return snake_body, score, food_spawn, speed_up, reward