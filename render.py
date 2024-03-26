import time
import argparse

import gym
from env.environment import GreedySnakeEnv
from stable_baselines3 import DQN


# args
def args_parser():
    parser = argparse.ArgumentParser("Greedy Snake", add_help = False)
    
    parser.add_argument("--gpu", default = "cuda:0", type = str)
    parser.add_argument("--window_size_x", default = 200, type = int)
    parser.add_argument("--window_size_y", default = 200, type = int)
    parser.add_argument("--speed", default = 200, type = float)
    parser.add_argument("--checkpoint", default = "checkpoint/rl_model_50000000_steps.zip", type = str)
    parser = parser.parse_args()

    return parser

args = args_parser()


def main():
    gym.register(
        id = 'GreedySnake-v0',
        entry_point = 'environment:GreedySnakeEnv', 
        kwargs = {'args': args}
    )

    env = gym.make('GreedySnake-v0', args = args)
    obs = env.reset()
    model = DQN.load(args.checkpoint, env = env, device = args.gpu)

    done = False
    while True:
        action, _states = model.predict(obs, deterministic = True)
        obs, reward, done, truncated = env.step(action)
        if done or truncated:
            obs = env.reset()
        env.render()
        time.sleep(0.05)
    env.close()


if __name__ == '__main__':
    main()