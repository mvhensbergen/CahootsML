import random

from cahoots import Game
from players import Player
from gymnasium import spaces

import gymnasium as gym

REWARDS = {
    "INVALID_MOVE": -1,
    "VALID_MOVE": 0,
    "MISSION_ACCOMPLISHED": 0,
    "WON_GAME": 10,
    "LOST_GAME": -10,
}


class CahootsEnv(gym.Env):
    def __init__(self, render_mode, number_of_players, number_of_missions, outdir):
        self.render_mode = render_mode
        self.number_of_missions = number_of_missions

        players = []
        for no in range(0, number_of_players):
            players.append(Player(f"Player {no}"))

        self.cahoots = Game(
            players=players, number_of_missions=self.number_of_missions, outdir=outdir
        )

        self.cahoots.reset()
        self.cahoots.id = 0  # FIXME ugly

        self.num_cards = len(self.cahoots.allcards) + 1
        self.total_possible_missions = self.cahoots.total_possible_missions + 1

        # FIXME: what about played cards?
        self.observation_space = spaces.Dict(
            {
                "player_cards": spaces.Tuple(
                    (
                        spaces.Discrete(self.num_cards, start=-1),
                        spaces.Discrete(self.num_cards, start=-1),
                        spaces.Discrete(self.num_cards, start=-1),
                        spaces.Discrete(self.num_cards, start=-1),
                    )
                ),
                "current_missions": spaces.Tuple(
                    (
                        spaces.Discrete(self.total_possible_missions, start=-1),
                        spaces.Discrete(self.total_possible_missions, start=-1),
                        spaces.Discrete(self.total_possible_missions, start=-1),
                        spaces.Discrete(self.total_possible_missions, start=-1),
                    )
                ),
                "table_cards": spaces.Tuple(
                    (
                        spaces.Discrete(self.num_cards),
                        spaces.Discrete(self.num_cards),
                        spaces.Discrete(self.num_cards),
                        spaces.Discrete(self.num_cards),
                    )
                ),
            }
        )

        self.action_space = spaces.Discrete(16)

    def _get_obs(self):
        obs = self.observation_space.sample()

        t = list(obs["current_missions"])
        for index, m in enumerate(self.cahoots.missions):
            if m:
                val = m.id
            else:
                val = -1
            t[index] = val
        obs["current_missions"] = tuple(t)

        t = list(obs["table_cards"])
        for index, c in enumerate(self.cahoots.table_cards):
            if c:
                val = c.id
            else:
                val = -1
            t[index] = val
        obs["table_cards"] = tuple(t)

        t = list(obs["player_cards"])
        for index, c in enumerate(self.cahoots.players[0].cards):
            if c:
                val = c.id
            else:
                val = -1
            t[index] = val
        obs["player_cards"] = tuple(t)

        return obs

    def action_to_src_dest(self, action):
        src = int(action / 4)
        dst = action - int(action / 4) * 4
        return [src, dst]

    def step(self, action):
        terminated = False
        solved_mission_count = 0

        [src, dst] = self.action_to_src_dest(action)

        reward = 0

        # If the player has no possible moves, switch to the next player
        if self.cahoots.count_moves() == 0:
            self.cahoots.finish_turn()
        else:
            # If the player chooses a non-valid move, give reward
            # and make the player choose a new move
            if not self.cahoots.valid_move(src, dst):
                # print ("Invalid")
                reward = REWARDS["INVALID_MOVE"]
                self.cahoots.finish_turn(valid_move=False)
            else:
                # If the player chooses a valid move, update the state of the game
                self.cahoots.do_move(src, dst)
                solved_mission_count = self.cahoots.finish_turn()
                reward = REWARDS["VALID_MOVE"]
                reward += REWARDS["MISSION_ACCOMPLISHED"] * solved_mission_count

        # Check for the end conditions of the game
        state = self.cahoots.get_stats()
        if state["finished"]:
            terminated = True
            if len(state["missions_remaining"]) == 0:
                reward += REWARDS["WON_GAME"]
                # print ("WON!")
            else:
                reward += REWARDS["LOST_GAME"]
                # print ("LOST!")

        observation = self._get_obs()

        if self.render_mode:
            self.render()

        return observation, reward, terminated, False, state

    def render(self):
        self.cahoots.print()

    def set_render(self, mode):
        self.render_mode = mode

    def reset(self, seed=None, options=None):
        if seed:
            random.seed(seed)

        self.cahoots.reset()

        return self._get_obs(), None
