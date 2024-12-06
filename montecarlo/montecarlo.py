import numpy as np
import pandas as pd

class Die:
    """A die has  𝑁 sides, or “faces”, and  𝑊 weights, and can be rolled to select a face. For example, a “die” with  𝑁=2 is a coin, and a one with  𝑁=6 is a standard die. 
    Normally, dice and coins are “fair,” meaning that the each side has an equal weight. An unfair die is one where the weights are unequal. 
    Each side contains a unique symbol. Symbols may be all alphabetic or all numeric. 𝑊 defaults to  1.0 for each face but can be changed after the object is created. 
    The weights are just positive numbers (integers or floats, including  0), not a normalized probability distribution. The die has one behavior, which is to be rolled one or more times"""
    def __init__(self, N):
        """Takes a NumPy array of faces as an argument. Throws a TypeError if not a NumPy array. The array’s data type dtype may be strings or numbers. 
        The array’s values must be distinct. Tests to see if the values are distinct and raises a ValueError if not. 
        Internally initializes the weights to  1.0 for each face. Saves both faces and weights in a private data frame with faces in the index."""
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
        """Takes two arguments: the face value to be changed and the new weight. Checks to see if the face passed is valid value, i.e. if it is in the die array. 
        If not, raises an IndexError. Checks to see if the weight is a valid type, i.e. if it is numeric (integer or float) or castable as numeric. If not, raises a TypeError"""
        if not face in set(self.df["Face"]):
            raise ValueError("Such a face is not found carved unto this die!")
        self.df.loc[self.df['Face'] == face, 'Weight'] = W
        total_weight = self.df["Weight"].sum()
        self.df["Probability"] = self.df["Weight"] / total_weight

    def roll(self, count=1):
        """Takes a parameter of how many times the die is to be rolled; defaults to  1. This is essentially a random sample with replacement, from the private die data frame, that applies the weights. 
        Returns a Python list of outcomes. Does not store internally these results."""
        fate_of_the_roll = np.random.choice(self.df['Face'], size=count, p=self.df['Probability'])
        return list(fate_of_the_roll)
    
    def characteristics(self):
        """Returns a copy of the private die data frame."""
        return self.df
    
    def get_name(self):
        """Returns the name of the variable holding the instance"""
        for name, obj in globals().items():
            if obj is self:
                return name
        return "Unknown Die"  

class Game:
    """This  game consists of rolling of one or more similar dice (Die objects) one or more times.By similar dice, each die in a given game has the same number of sides and associated faces, but each die object may have its own weights. 
    Each game is initialized with a Python list that contains one or more dice. Game objects have a behavior to play a game, i.e. to roll all of the dice a given number of times.Game objects only keep the results of their most recent play"""
    def __init__(self, dice):
        """Takes a single parameter, a list of already instantiated similar dice. Ideally this would check if the list actually contains Die objects and that they all have the same faces, but this is not required for this project."""
        self.first_die = dice[0].df['Face'].values
        if not all(np.array_equal(die.df['Face'].values, self.first_die) for die in dice):
            raise TypeError("Halt! Thou must present matching dice!")
        self.bag_of_dice = dice
        self.previous_game = None
        
    def play(self, rolls):
        """Takes an integer parameter to specify how many times the dice should be rolled. Saves the result of the play to a private data frame. 
        The data frame should be in wide format, i.e. have the roll number as a named index, columns for each die number (using its list index as the column name), and the face rolled in that instance in each cell."""
        roll_log = []
        for i, die in enumerate(self.bag_of_dice, 1):
            roll_result = die.roll(rolls)
            roll_result_list = list(roll_result)
            roll_log.append([die.get_name()] + roll_result_list)
        column_names = ['Die'] + [f'Roll {i+1}' for i in range(rolls)]
        self.previous_game = pd.DataFrame(roll_log, columns=column_names)
        
    def recall(self, shape="wide"):
        """This method just returns a copy of the private play data frame to the user. Takes a parameter to return the data frame in narrow or wide form which defaults to wide form. 
        The narrow form has a MultiIndex, comprising the roll number and the die number (in that order), and a single column with the outcomes (i.e. the face rolled).
        This method raises a ValueError if the user passes an invalid option for narrow or wide."""
        if shape.lower() == "wide":
            return self.previous_game
        if shape.lower() == "narrow":
            return self.previous_game.set_index("Die").T
        else:
            raise TypeError("Enter a valid shape!")
    
    def provide_faces(self):
        """This method simply returns the array of faces from the first die in the set to allow for use in a child class without setting up a hierarchy. Seeing as all dice must be similar, using any instance of a dice will represent all dice."""
        return self.first_die

class Analyzer:
    """This Analyzer object takes the results of a single game and computes various descriptive statistical properties about it such as weather the user rolled equal faces on all dice,
    how manytimes each face was rolled, how many uniquie combinations of faces were rolled (both independendent and dependent order)."""
    def __init__(self, game_object):
        """Takes a game object as its input parameter. Throws a ValueError if the passed value is not a Game object."""
        if not isinstance(game_object, Game):
            raise ValueError("Not a valid Game object!")
        self.game_object = game_object
        self.recall_wide = self.game_object.recall()
        self.recall_narrow = self.game_object.recall("narrow")

    def jackpot(self):
        """A jackpot is a result in which all faces are the same, e.g. all ones for a six-sided die. Computes how many times the game resulted in a jackpot.Returns an integer for the number of jackpots."""
        jackpots = 0
        for i, row in self.recall_narrow.iterrows():
            if len(set(row)) == 1:
                jackpots += 1
        return jackpots
    
    def face_counts(self):
        """Computes how many times a given face is rolled in each event. For example, if a roll of five dice has all sixes, then the counts for this roll would be 5 for the face value ‘6’ and  0 for the other faces. 
        Returns a data frame of results.The data frame has an index of the roll number, face values as columns, and count values in the cells (i.e. it is in wide format)."""
        face_values = self.game_object.provide_faces()
        face_counts = pd.DataFrame(columns=face_values)
        for i, row in self.recall_narrow.iterrows():
            count = {face: row.tolist().count(face) for face in face_values}
            face_counts.loc[i] = count
        return face_counts

    def combo_count(self):
        """Computes the distinct combinations of faces rolled, along with their counts. Combinations are order-independent and may contain repetitions. 
        Returns a data frame of results. The data frame should has a MultiIndex of distinct combinations and a column for the associated counts."""
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
        """Computes the distinct permutations of faces rolled, along with their counts.
        Permutations are order-dependent and may contain repetitions. Returns a data frame of results. The data frame should have a MultiIndex of distinct permutations and a column for the associated counts."""
        permutations_list = []
        for index, row in self.recall_narrow.iterrows():
            roll_values = row.values
            permutations_list.append(roll_values)
        permutations_df = pd.DataFrame(permutations_list)
        permutations_df.columns = [f'Value{i+1}' for i in range(permutations_df.shape[1])]
        permutation_counts = permutations_df.groupby(list(permutations_df.columns)).size().reset_index(name='Count')
        permutation_counts.set_index(list(permutations_df.columns), inplace=True) 
        return permutation_counts
