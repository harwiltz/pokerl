import gym
import numpy as np
import random

class MRLPokerEnv(gym.Env):
    bet = 0
    fold = 1
    call = 2

    is_fold = lambda a: a < 0
    is_call = lambda a: a == 0
    is_bet  = lambda a: a > 0

    def __init__(self, dealer=False, chips=1000, rounds=1000, betting_rounds=3, max_bet=1000, bet_scale=2):
        self.dealer = dealer
        self.start_chips = chips
        self.rounds = rounds
        self.max_bet = max_bet
        self.betting_rounds = betting_rounds
        self.bet_scale = bet_scale

        # This designates what goes in each dimension of the state space
        self.state_keys = [('card', 0, 1),                          # float [0,1]
                           ('chips', 0, 2*chips),                   # float [0,chips]
                           ('rounds_remaining', 0, betting_rounds), # int [betting_rounds]
                           ('min_bet', 0, max_bet),                 # float [0, max_bet]
                           ('pot', 0, 2*chips),                     # float [0,\infty]
                           ('opp_chips', 0, 2*chips)]               # float [0,chips]
        self.state_dim = len(self.state_keys)
        obs_low = np.array([x[1] for x in self.state_keys], dtype=np.float32)
        obs_high = np.array([x[2] for x in self.state_keys], dtype=np.float32)
        self.observation_space = gym.spaces.Box(obs_low,
                                                obs_high)
        self.action_space = gym.spaces.Box(np.zeros(1), np.array((max_bet,)))

        self.last_bet = None
        self.reset()

    def step(self, player, action):
        """
        Fold: -1 (or < 0)
        Call/Check: 0
        Raise/Bet: total bet - 2 * min_bet + 1 (The +1 allows for min raise)
        bet = min_bet + min_bet + x
        """
        done = False
        action = int(action)
        if MRLPokerEnv.is_fold(action):
            self.end_betting_round(player, action)
            done = True
        else:
            bet = (MRLPokerEnv.is_bet(action) * (2 * self.min_bet + (action - 1))
                   + MRLPokerEnv.is_call(action) * self.min_bet)
            bet = np.min([bet, self.max_bet, *self.chips])
            self.chips[player] -= bet
            self.pot += bet
            if (self.last_bet is not None) and (self.last_bet == bet):
                self.end_betting_round(player, action)
            else:
                self.min_bet = bet
            self.last_bet = bet
        state = self.get_state(1^player)
        done = done or (self.betting_round == self.betting_rounds)
        return state, self.chips[player], done, {'keys': self.state_keys}

    def get_state(self, player):
        state_array = [self.cards[player],
                       self.chips[player],
                       self.betting_rounds - self.betting_round + 1,
                       self.min_bet,
                       self.pot,
                       self.chips[1^player]]
        return np.array(state_array, dtype=np.float32)

    def is_betting_round_finished(self, player, action):
        return self.last_bet is None

    def end_betting_round(self, player, action):
        winner = self.determine_winner(player, action)
        if winner is None:
            self.chips += int(self.pot / 2)
        else:
            self.chips[winner] += self.pot
        self.pot = 0
        self.min_bet = 0
        self.betting_round += 1
        self.last_bet = None

    def determine_winner(self, player, action):
        winner = None
        if MRLPokerEnv.is_fold(action):
            winner = 1^player
        elif self.cards[0] > self.cards[1]:
            winner = 0
        elif self.cards[1] > self.cards[0]:
            winner = 1
        return winner

    def reset(self, new_match=False):
        self.min_bet = 0
        self.pot = 0
        self.cur_round = 1
        self.betting_round = 0
        self.last_bet = None
        self.state = np.zeros(self.state_dim, dtype=np.float32)
        self.chips = np.array([self.start_chips, self.start_chips], dtype=np.int32)
        self.cards = [random.random(), random.random()]
