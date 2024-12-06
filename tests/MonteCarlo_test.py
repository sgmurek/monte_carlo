import numpy as np
import pandas as pd
import unittest

class Die:
    def __init__(self, N):
        if not isinstance(N, np.ndarray):
            raise TypeError("Halt! Thou hast not brought an array!")
        self.is_distinct = (lambda x: len(x) == len(set(x)))(N)
        if not self.is_distinct:
            raise ValueError("Halt! Thy die must bear distinct faces!")
        self.weighted_array = np.ones(len(N), dtype=float)
        self.die = N
        self.df = pd.DataFrame({'Face': N, 'Weight': self.weighted_array})
        self.df['Probability'] = self.df["Weight"] / self.df["Weight"].sum()
    
    def cheat(self, face, W):
        if not face in set(self.df["Face"]):
            raise ValueError("Such a face is not found carved unto this die!")
        self.df.loc[self.df['Face'] == face, 'Weight'] = W
        total_weight = self.df["Weight"].sum()
        self.df["Probability"] = self.df["Weight"] / total_weight

    def roll(self, count=1):
        fate_of_the_roll = np.random.choice(self.df['Face'], size=count, p=self.df['Probability'])
        return list(fate_of_the_roll)
    
    def characteristics(self):
        return self.df
    
    def get_name(self):
        for name, obj in globals().items():
            if obj is self:
                return name
        return "Unknown Die"  

class Game:
    def __init__(self, dice):
        self.first_die = dice[0].df['Face'].values
        if not all(np.array_equal(die.df['Face'].values, self.first_die) for die in dice):
            raise TypeError("Halt! Thou must present matching dice!")
        self.bag_of_dice = dice
        self.previous_game = None
        
    def play(self, rolls):
        roll_log = []
        for i, die in enumerate(self.bag_of_dice, 1):
            roll_result = die.roll(rolls)
            roll_result_list = list(roll_result)
            roll_log.append([die.get_name()] + roll_result_list)
        column_names = ['Die'] + [f'Roll {i+1}' for i in range(rolls)]
        self.previous_game = pd.DataFrame(roll_log, columns=column_names)
        
    def recall(self, shape="wide"):
        if shape.lower() == "wide":
            return self.previous_game
        if shape.lower() == "narrow":
            return self.previous_game.set_index("Die").T
        else:
            raise TypeError("Enter a valid shape!")
    
    def provide_faces(self):
        return self.first_die

class Analyzer:
    def __init__(self, game_object):
        if not isinstance(game_object, Game):
            raise ValueError("Not a valid Game object!")
        self.game_object = game_object
        self.recall_wide = self.game_object.recall()
        self.recall_narrow = self.game_object.recall("narrow")

    def jackpot(self):
        jackpots = 0
        for i, row in self.recall_narrow.iterrows():
            if len(set(row)) == 1:
                jackpots += 1
        return jackpots
    
    def face_counts(self):
        face_values = self.game_object.provide_faces()
        face_counts = pd.DataFrame(columns=face_values)
        for i, row in self.recall_narrow.iterrows():
            count = {face: row.tolist().count(face) for face in face_values}
            face_counts.loc[i] = count
        return face_counts

    def combo_count(self):
        combinations_list = []
        for index, row in self.recall_narrow.iterrows():
            roll_values = sorted(row.values)
            combinations_list.append(roll_values)
        combinations_df = pd.DataFrame(combinations_list)
        combinations_df.columns = [f'Value{i+1}' for i in range(combinations_df.shape[1])]
        combo_counts = combinations_df.groupby(list(combinations_df.columns)).size().reset_index(name='Count')
        combo_counts.set_index(list(combinations_df.columns), inplace=True) 
        return combo_counts

    def permutation_count(self):
        permutations_list = []
        for index, row in self.recall_narrow.iterrows():
            roll_values = row.values
            permutations_list.append(roll_values)
        permutations_df = pd.DataFrame(permutations_list)
        permutations_df.columns = [f'Value{i+1}' for i in range(permutations_df.shape[1])]
        permutation_counts = permutations_df.groupby(list(permutations_df.columns)).size().reset_index(name='Count')
        permutation_counts.set_index(list(permutations_df.columns), inplace=True) 
        return permutation_counts


class MonteCarloTestSuite(unittest.TestCase):
        
    def setUp(self):
        self.Valid_Die_6_Sides = Die(np.arange(1, 7))
        self.Valid_Die_2_Sides = Die(np.arange(1, 3))
        self.Valid_Game = Game([self.Valid_Die_6_Sides, self.Valid_Die_6_Sides])
        
        # Call play()
        self.Valid_Game.play(3)
        #initialize the Analyzer
        self.Valid_Analyzer = Analyzer(self.Valid_Game)
    
    def test_Die_init(self):
        with self.assertRaises(TypeError):
            Die([1, 2, 3])

    def test_Die_cheat(self):
        self.Weighted_Die = Die(self.Valid_Die_6_Sides.die)
        self.Weighted_Die.cheat(4, 10)
        self.assertTrue(self.Weighted_Die.characteristics()['Weight'].iloc[3] == 10)
        
    def test_Die_characteristics(self):
        self.assertIsInstance(self.Valid_Die_6_Sides.characteristics(), pd.DataFrame) 

    def test_Game_init(self):
        with self.assertRaises(TypeError):
            Game([self.Valid_Die_6_Sides, self.Valid_Die_2_Sides])

    def test_Game_recall(self):
        self.assertIsInstance(self.Valid_Game.recall("wide"), pd.DataFrame)

    def test_Game_provide_faces(self):
        self.assertIsInstance(self.Valid_Game.provide_faces(), np.ndarray)

    def test_Analyzer_init(self):
        with self.assertRaises(ValueError):
            Analyzer(self.Valid_Die_6_Sides)

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
