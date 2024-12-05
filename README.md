# Final Project - Monte Carlo Simulator

##  DS5100-wsr7qr,  Shawn Gmurek 
### Last Updated on 12/5/2024

## Contents
This Branch contains the relevent resources for the Monte Carlo package needed for this final project. 

## Synopsis
The purpose of this package is to create three classes:
- A Die class
- A Game class
- An Analyzer class

The Die class allows a player to create a die for every object they wish to create. The die must be submitted as an array, but that array can be anything they would like and as large as they would like. The user may weight these die if they so please by calling upon the cheat method. 
This class also contains a roll method that is referenced in a later class, a characteristics method that returns the dataframe containing the die and its weights, and a get_name method that is used to keep track of die names.

The Game class allows the player to bring forth a list of dice objects from the Die class and pass them through a game. This class allows the users to bring forth variously weight dice, but expects them to be of the same faces and face count. The user speciies how many times they would like the dice to roll by entering an integer into the play method. If the player wishes to reference their last game further down the road, the recall method will store the player's most recent roll for them to reference at their convenience.

The Analyzer class contains statistical information regarding a players game. It accepts a Game object and allows for the player to view how many times they rolled a matching set of dice, how many times each face was rolled in a hand, how many combinations of dice they rolled, and a count of ordered combinations they rolled.

## API
***Classes:***
  Die: 
  """A die has  𝑁 sides, or “faces”, and  𝑊 weights, and can be rolled to select a face. For example, a “die” with  𝑁=2 is a coin, and a one with  𝑁=6 is a standard die. 
    Normally, dice and coins are “fair,” meaning that the each side has an equal weight. An unfair die is one where the weights are unequal. 
    Each side contains a unique symbol. Symbols may be all alphabetic or all numeric. 𝑊 defaults to  1.0 for each face but can be changed after the object is created. 
    The weights are just positive numbers (integers or floats, including  0), not a normalized probability distribution. The die has one behavior, which is to be rolled one or more times"""
    
     e.x. of how to initialize: Fair_Coin = Die(np.array(['H','T']))
  Game:
    """This  game consists of rolling of one or more similar dice (Die objects) one or more times.
    By similar dice, each die in a given game has the same number of sides and associated faces, but each die object may have its own weights. 
    Each game is initialized with a Python list that contains one or more dice. 
    Game objects have a behavior to play a game, i.e. to roll all of the dice a given number of times.Game objects only keep the results of their most recent play"""
    
     e.x. of how to initialize: Game1 = Game([Fair_Coin,Fair_Coin])

  Analyzer:
  """This Analyzer object takes the results of a single game and computes various descriptive statistical properties about it such as weather the user rolled equal faces on all dice,
    how manytimes each face was rolled, how many uniquie combinations of faces were rolled (both independendent and dependent order)."""
    
        e.x. of how to initialize: Analyze1 = Analyzer(Game1)
    
***Methods:***
  Die:
    __init__():
    """Takes a NumPy array of faces as an argument. Throws a TypeError if not a NumPy array. The array’s data type dtype may be strings or numbers. 
    The array’s values must be distinct. Tests to see if the values are distinct and raises a ValueError if not. 
    TInternally initializes the weights to  1.0 for each face. Saves both faces and weights in a private data frame with faces in the index."""

   cheat():
   """Takes two arguments: the face value to be changed and the new weight. Checks to see if the face passed is valid value, i.e. if it is in the die array. 
   If not, raises an IndexError. Checks to see if the weight is a valid type, i.e. if it is numeric (integer or float) or castable as numeric. If not, raises a TypeError"""

   roll():
   """Takes a parameter of how many times the die is to be rolled; defaults to  1. This is essentially a random sample with replacement, from the private die data frame, that applies the weights.
   Returns a Python list of outcomes. Does not store internally these results."""

   characteristics():
   """Returns a copy of the private die data frame."""

   get_name():
   """Returns the name of the variable holding the instance"""

  Game:
  __init__():
  """Takes a single parameter, a list of already instantiated similar dice. Ideally this would check if the list actually contains Die objects and that they all have the same faces, but this is not required for this project."""

  play():
  """Takes an integer parameter to specify how many times the dice should be rolled. Saves the result of the play to a private data frame. 
  The data frame should be in wide format, i.e. have the roll number as a named index, columns for each die number (using its list index as the column name), and the face rolled in that instance in each cell."""

  recall():
  """This method just returns a copy of the private play data frame to the user. Takes a parameter to return the data frame in narrow or wide form which defaults to wide form. 
  The narrow form has a MultiIndex, comprising the roll number and the die number (in that order), and a single column with the outcomes (i.e. the face rolled).
  This method raises a ValueError if the user passes an invalid option for narrow or wide."""

  provie_faces()
  """This method simply returns the array of faces from the first die in the set to allow for use in a child class without setting up a hierarchy. Seeing as all dice must be similar, using any instance of a dice will represent all dice."""

  Analyzer:
  __init__():

  jackpot():
  """A jackpot is a result in which all faces are the same, e.g. all ones for a six-sided die. Computes how many times the game resulted in a jackpot.Returns an integer for the number of jackpots."""

  face_counts():
  """Computes how many times a given face is rolled in each event. For example, if a roll of five dice has all sixes, then the counts for this roll would be 5 for the face value ‘6’ and  0 for the other faces. 
  Returns a data frame of results.The data frame has an index of the roll number, face values as columns, and count values in the cells (i.e. it is in wide format)."""

  combo_count():
  """Computes the distinct combinations of faces rolled, along with their counts. Combinations are order-independent and may contain repetitions. 
  Returns a data frame of results. The data frame should has a MultiIndex of distinct combinations and a column for the associated counts."""

  permutation_count():
  """Computes the distinct permutations of faces rolled, along with their counts.
  Permutations are order-dependent and may contain repetitions. Returns a data frame of results. The data frame should have a MultiIndex of distinct permutations and a column for the associated counts."""

How to install this package:
  In your shell, enter:
    pip install git+https://github.com/sgmurek/DS5100-wsr7qr/final_project.git
