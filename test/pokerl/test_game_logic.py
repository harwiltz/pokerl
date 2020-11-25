import unittest

from pokerl.env import MRLPokerEnv

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        self.env_1_round = MRLPokerEnv(False, betting_rounds=1)
        self.env_3_round = MRLPokerEnv(False, betting_rounds=3)
        self.env_1_round.reset()
        self.env_3_round.reset()

    def test_1_round_check(self):
        ns, r, d, info = self.env_1_round.step(0, 0)
        self.assertEqual(self.env_1_round.pot, 0)
        self.assertEqual(r, 1000)
        self.assertFalse(d)

    def test_1_round_bet(self):
        ns, r, d, info = self.env_1_round.step(0, 3)
        self.assertEqual(self.env_1_round.pot, 2)
        self.assertEqual(r, 998)
        self.assertFalse(d)

    def test_1_round_checkcheck(self):
        self.env_1_round.step(0, 0)
        ns, r, d, info = self.env_1_round.step(1, 0)
        self.assertEqual(self.env_1_round.pot, 0)
        self.assertEqual(r, 1000)
        self.assertTrue(d)

    def test_1_round_call(self):
        self.env_1_round.cards = [0.5, 0.6]
        self.env_1_round.step(0, 0) # Check
        self.env_1_round.step(1, 3) # Bet 2
        ns, r, d, _ = self.env_1_round.step(0, 0) # Call
        self.assertTrue(d)
        self.assertEqual(self.env_1_round.pot, 0) # Pot already distributed
        self.assertEqual(self.env_1_round.chips[0], 998)
        self.assertEqual(self.env_1_round.chips[1], 1002)

    def test_1_round_draw(self):
        self.env_1_round.cards = [0.5, 0.5]
        self.env_1_round.step(0, 0) # Check
        self.env_1_round.step(1, 3) # Bet 2
        ns, r, d, _ = self.env_1_round.step(0, 0) # Call
        self.assertTrue(d)
        self.assertEqual(self.env_1_round.pot, 0)
        self.assertEqual(self.env_1_round.chips[0], 1000)
        self.assertEqual(self.env_1_round.chips[1], 1000)

    def test_1_round_fold(self):
        self.env_1_round.step(0, 5) # Bet 4
        self.env_1_round.step(1, 1) # Bet 8
        ns, r, d, _ = self.env_1_round.step(0,-1) # Fold
        self.assertTrue(d)
        self.assertEqual(self.env_1_round.pot, 0)
        self.assertEqual(self.env_1_round.chips[0], 996)
        self.assertEqual(self.env_1_round.chips[1], 1004)

    def test_3_round_fold_early(self):
        self.env_3_round.step(0, 5) # Bet 4
        self.env_3_round.step(1, 1) # Bet 8
        ns, r, d, _ = self.env_3_round.step(0,-1) # Fold
        self.assertTrue(d)
        self.assertEqual(self.env_3_round.pot, 0)
        self.assertEqual(self.env_3_round.chips[0], 996)
        self.assertEqual(self.env_3_round.chips[1], 1004)

if __name__ == "__main__":
    unittest.main()
