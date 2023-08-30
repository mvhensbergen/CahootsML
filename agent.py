from collections import defaultdict
import random
import numpy as np


class Agent:
    def __init__(
        self,
        env,
        learning_rate: float,
        initial_epsilon: float,
        epsilon_decay: float,
        final_epsilon: float,
        discount_factor: float,
        initial_value: float,
    ):
        self.lr = learning_rate
        self.discount_factor = discount_factor

        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon
        self.q_values = defaultdict(
            lambda: np.full(env.action_space.n, self.initial_value)
        )

        self.initial_value = initial_value

        self.training_error = []

    def get_action(self, env, obs):
        dice = random.random()
        if dice < self.epsilon:
            return env.action_space.sample(), 0
        else:
            obs = str(obs)

            m = np.max(self.q_values[obs])
            action = random.choice(np.where(self.q_values[obs] == m)[0])
            return action, 1

    def update(self, env, obs, action, reward, terminated, next_obs):
        """Updates the Q-value of an action."""
        # Convert obs and next_obs to hashable structs
        obs = str(obs)
        next_obs = str(next_obs)

        future_q_value = (not terminated) * np.max(self.q_values[next_obs])
        temporal_difference = (
            reward + self.discount_factor * future_q_value - self.q_values[obs][action]
        )

        self.q_values[obs][action] = (
            self.q_values[obs][action] + self.lr * temporal_difference
        )
        self.training_error.append(temporal_difference)

    def decay_epsilon(self):
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)
