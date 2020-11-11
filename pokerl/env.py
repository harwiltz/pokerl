import gym
import numpy as np
import random

class MRLPokerEnv(gym.Environment):
    def __init__(self, agents, dealer=False, chips=1000, rounds=1000, betting_rounds=3, max_bet=1000):
        self.agents = agents
        self.dealer = dealer
        self.chips = float(chips)
        self.rounds = rounds
        self.max_bet = float(max_bet)
        self.betting_rounds = betting_rounds
        self.reset(new_match=True)
        self.observation_space = gym.spaces.Box(np.array((0.0,)), np.array((1.0,)))
        self.action_space = gym.spaces.Box(np.array((0.0,)), np.array((self.max_bet,)))

    def step(self, player, action):
        move, amount = action
        amount = float(min(amount, self.max_bet))
        done = False
        if move == MRLPokerEnv.fold:
            done = True
            self.chips[1^player] += self.pot
        elif move == MRLPokerEnv.bet:
            if self.is_legal_bet(amount):
                self.chips[player] -= amount
                self.pot += amount
                self.min_bet = amount
            else:
                done = True
                self.chips[1^player] += self.pot
        elif not self.is_legal_bet(0):
            done = True
            self.chips[1^player] += self.pot
        self.update_state()
        return self.state

    def is_legal_bet(self, amount):
        if amount < self.min_bet:
            return False
        if amount > self.max_bet:
            return False
        return True

    def update_state(self):
        pass

    def reset(self, new_match=False):
        self.cur_round = 1
        self.cur_betting_round = 1
        self.pot = 0.0
        self.min_bet = 0.0
        self.state = None # TODO: figure out state space
        if new_match:
            self.chip_stacks = [self.chips for _ in self.agents]
            self.cards = [random.random(), random.random()]
