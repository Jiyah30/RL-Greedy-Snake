import os
import argparse

import gym
import pygame
from env.environment import GreedySnakeEnv
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import CheckpointCallback, EveryNTimesteps
from stable_baselines3.common.vec_env.util import copy_obs_dict, dict_to_obs, obs_space_info

os.environ["SDL_VIDEODRIVER"] = "dummy"

def args_parser():
    parser = argparse.ArgumentParser("Greedy Snake", add_help = False)
    
    # basic
    parser.add_argument("--window_size_x", default = 100, type = int)
    parser.add_argument("--window_size_y", default = 100, type = int)
    parser.add_argument("--speed", default = 200, type = float)

    parser.add_argument("--checkpoint_save_freq", default = 1, type = int)
    parser.add_argument("--checkpoint_path", default = "./checkpoint/", type = str)
    parser.add_argument("--callback_n_steps", default = 10000, type = int)

    # model
    parser.add_argument("--policy", default = "MlpPolicy", type = str)
    parser.add_argument("--total_timesteps", default = 1000000, type = int)
    parser.add_argument("--batch_size", default = 512, type = int)
    parser.add_argument("--tau", default = 0.95, type = float)
    parser.add_argument("--exploration_fraction", default = 0.5, type = float)
    parser.add_argument("--tensorboard_log_path", default = "./tensorboard_log/", type = str)
    parser.add_argument("--log_interval", default = 4, type = int)

    parser = parser.parse_args()

    return parser

args = args_parser()


def main():
    
    gym.register(
        id = 'GreedySnake-v0',
        entry_point = 'environment:GreedySnakeEnv', 
        kwargs = {'args': args}
    )

    checkpoint_on_event = CheckpointCallback(save_freq = args.checkpoint_save_freq, save_path = args.checkpoint_path)
    event_callback = EveryNTimesteps(n_steps = args.callback_n_steps, callback = checkpoint_on_event)

    env = gym.make('GreedySnake-v0', args = args)

    model = DQN(args.policy, env, verbose = 1, batch_size = args.batch_size, tau = args.tau, 
                exploration_fraction = args.exploration_fraction, tensorboard_log = args.tensorboard_log_path)
    model.learn(total_timesteps = args.total_timesteps, callback = event_callback, log_interval = args.log_interval)
    model.save("GreedySnake")

if __name__ == '__main__':
    main()
    pygame.quit()