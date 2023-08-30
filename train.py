import numpy as np
import os

import gymnasium as gym
from cahootsenv import CahootsEnv

import matplotlib.pyplot as plt
from tqdm import tqdm

from agent import Agent

import argparse


class DefaultHelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter
):
    pass


def training_section(parser):
    training_group = parser.add_argument_group("Training Configuration")
    training_group.add_argument(
        "--episodes", help="number of games (episodes) to play", default=20000, type=int
    )
    training_group.add_argument(
        "--seed",
        help="Seed to use (0 for no seed); fixed seed trains the game on exactly the same card and missions each episode",
        default=42,
        type=int,
    )
    training_group.add_argument(
        "--render-percentage",
        help="Start rendering the output of the games after this many percent of rounds have been played",
        default=99.9,
        type=float,
    )
    training_group.add_argument(
        "--outdir", help="Output directory for screenshots if set", default=None
    )


def agent_section(parser):
    agent_group = parser.add_argument_group("Agent Configuration")
    agent_group.add_argument(
        "--learning_rate", help="Learning rate", default=0.01, type=float
    )
    agent_group.add_argument(
        "--start_epsilon", help="Start greedy epsilon", default=1, type=float
    )
    agent_group.add_argument(
        "--final_epsilon", help="Final greedy epsilon", default=0.1, type=float
    )
    agent_group.add_argument(
        "--discount_factor", help="Discount factor", default=0.95, type=float
    )
    agent_group.add_argument(
        "--initial", help="Initial learning value", default=1000.0, type=float
    )


def cahoots_section(parser):
    cahoots_group = parser.add_argument_group("Cahoots Configuration")
    cahoots_group.add_argument(
        "--missions", help="Number of missions", default=8, type=int
    )
    cahoots_group.add_argument(
        "--players", help="Number of players", default=2, type=int
    )


parser = argparse.ArgumentParser(formatter_class=DefaultHelpFormatter)
training_section(parser)
agent_section(parser)
cahoots_section(parser)

args = parser.parse_args()

for arg in vars(args):
    print(f"{arg}: {getattr(args, arg)}")

if args.outdir:
    if args.render_percentage >= 0 and args.render_percentage < 100:
        os.mkdir(args.outdir)
        print(f"Screenshots will be saved to dir '{args.outdir}'")
    else:
        print(
            f"Render percentage {args.render_percentage} is out of range - no screenshots will be made "
        )
else:
    print("No screenshot directory specified - no screenshots will be made")

num_render_p = args.render_percentage

env = CahootsEnv(
    render_mode=False,
    number_of_players=args.players,
    number_of_missions=args.missions,
    outdir=args.outdir,
)
env = gym.wrappers.RecordEpisodeStatistics(env, deque_size=args.episodes)

epsilon_decay = args.start_epsilon / (
    args.episodes / 2
)  # reduce the exploration over time
agent = Agent(
    env=env,
    learning_rate=args.learning_rate,
    initial_epsilon=args.start_epsilon,
    epsilon_decay=epsilon_decay,
    final_epsilon=args.final_epsilon,
    discount_factor=args.discount_factor,
    initial_value=float(args.initial),
)

total_wons = 0

for episode in tqdm(range(args.episodes)):
    i = 0
    obs, info = env.reset(seed=args.seed)
    done = False

    if episode >= args.episodes * num_render_p / 100:
        env.set_render(True)

    while not done:
        i += 1
        action, t = agent.get_action(env, obs)

        next_obs, reward, terminated, truncated, state = env.step(action)

        if len(state["missions_remaining"]) == 0:
            total_wons += 1

        # update the agent
        agent.update(env, obs, action, reward, terminated, next_obs)

        done = terminated or truncated
        obs = next_obs

    agent.decay_epsilon()


print("Total wons:", total_wons)

rolling_length = 50
fig, axs = plt.subplots(ncols=3, figsize=(12, 5))
axs[0].set_title("Episode rewards")
# compute and assign a rolling average of the data to provide a smoother graph
reward_moving_average = (
    np.convolve(
        np.array(env.return_queue).flatten(), np.ones(rolling_length), mode="valid"
    )
    / rolling_length
)
axs[0].plot(range(len(reward_moving_average)), reward_moving_average)
axs[1].set_title("Episode lengths")
length_moving_average = (
    np.convolve(
        np.array(env.length_queue).flatten(), np.ones(rolling_length), mode="same"
    )
    / rolling_length
)
axs[1].plot(range(len(length_moving_average)), length_moving_average)
axs[2].set_title("Training Error")
training_error_moving_average = (
    np.convolve(np.array(agent.training_error), np.ones(rolling_length), mode="same")
    / rolling_length
)
axs[2].plot(range(len(training_error_moving_average)), training_error_moving_average)
plt.tight_layout()
plt.show()
