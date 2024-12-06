import unittest
import numpy as np
import pandas as pd
import montecarlo as mc

class MonteCarloTestSuite(unittest.TestCase):
        
    def setUp(self):
        self.Valid_Die_6_Sides = mc.Die(np.arange(1, 7))
        self.Valid_Die_2_Sides = mc.Die(np.arange(1, 3))
        self.Valid_Game = mc.Game([self.Valid_Die_6_Sides, self.Valid_Die_6_Sides])
        
        #Call play() first to set the previous_game attribute
        self.Valid_Game.play(3)
        
        #initialize the Analyzer
        self.Valid_Analyzer = mc.Analyzer(self.Valid_Game)
    
    def test_Die_init(self):
        with self.assertRaises(TypeError):
            mc.Die([1, 2, 3])

    def test_Die_cheat(self):
        self.Weighted_Die = mc.Die(self.Valid_Die_6_Sides.die)
        self.Weighted_Die.cheat(4, 10)
        self.assertTrue(self.Weighted_Die.characteristics()['Weight'].iloc[3] == 10)
    
    def test_Die_roll(self):
        self.assertTrue(len(self.Valid_Die_6_Sides.roll(100)) ==100)
        
    def test_Die_characteristics(self):
        self.assertIsInstance(self.Valid_Die_6_Sides.characteristics(), pd.DataFrame) 

    def test_Game_init(self):
        with self.assertRaises(TypeError):
            mc.Game([self.Valid_Die_6_Sides, self.Valid_Die_2_Sides])

    def test_Game_recall(self):
        self.assertIsInstance(self.Valid_Game.recall("wide"), pd.DataFrame)

    def test_Game_provide_faces(self):
        self.assertIsInstance(self.Valid_Game.provide_faces(), np.ndarray)

    def test_Analyzer_init(self):
        with self.assertRaises(ValueError):
            mc.Analyzer(self.Valid_Die_6_Sides)

    def test_Analyzer_jackpot_dt(self):
        self.assertIsInstance(self.Valid_Analyzer.jackpot(), int)

    def test_Analyzer_face_counts(self):
        self.assertIsInstance(self.Valid_Analyzer.face_counts(), pd.DataFrame)
        
    def test_Analyzer_combo_count(self):
        self.assertIsInstance(self.Valid_Analyzer.combo_count(), pd.DataFrame)
            
    def test_Analyzer_permutation_count(self):
        self.assertIsInstance(self.Valid_Analyzer.permutation_count(), pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
