from Player import Player
import Deck
import keras
from keras import layers
import numpy as np
from collections import Counter


# Have this be a NN with 14 inputs (current card and how many of each playable card you have) and 14 outputs, 
# each output a probability of which card it should play and a "No possible plays option". 
# You can easily get training data by just getting a lot of scenarios and working out the lowest non-sepcial to play
# and stuff like that

# Also try to do this which has all cards, not just the playable ones

input_shape = (14,)
num_outputs = 14
model = keras.Sequential(
            [
                keras.Input(shape=input_shape),
                layers.Dense(20, activation="relu"),
                layers.Dense(20, activation="relu"),
                layers.Dense(num_outputs, activation="softmax"),
            ]
        )

print(model.summary())

class LowCostNNPlayer(Player):

    def __init__(self, i: int)-> None:
        super().__init__(i)
        
        global model
        model = keras.models.load_model('models/lowCostNN.keras')

    def choose_cards(self, playable_cards: list[int]) -> tuple[int]:
        print(f"For player {self.i} - {self.hand}")
        input = [Deck.get_current_card()]+[0]*13
        for card in playable_cards:
            input[card-1] = 1
        
        input = np.array([input])
        print(input)

        output = model.predict(input, verbose=0)
        c = Counter(playable_cards)
        print(c)

        card_output = int(np.argmax(output[0]))+1
        print(card_output)
        if c[card_output] == 0:
            raise ValueError("The LowCostNNPlayer is cheating, it is trying to use a card it doesn't have")
        return card_output, c[card_output]