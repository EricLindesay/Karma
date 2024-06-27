from LowCostNNPlayer import model
from LowCardPlayer import LowCardPlayer
import random
import Deck
import numpy as np
import json


def get_training_data(n: int) -> tuple[list, list]:
    x = []
    y = []
    player = LowCardPlayer(0)

    for i in range(n):
        Deck.init_deck()
        num_cards = random.randint(1, 12)
        random.shuffle(Deck.deck)

        player.hand = Deck.deck[:num_cards]
        top_card = random.randint(2, 14)

        Deck.pile = [top_card]
        playable_cards, _ = player.get_playable_cards()
        
        if len(playable_cards) > 0:
            card_played, _ = player.choose_cards(playable_cards)
        else:
            card_played = 1
        # Have this be a NN with 14 inputs (current card and how many of each playable card you have) and 15 outputs, 
        
        hand_cards = [top_card]+[0]*13
        for card in playable_cards:
            # hand_cards[card-1] += 1
            hand_cards[card-1] = 1

        y_value = [0]*14
        y_value[card_played-1] = 1

        x.append(hand_cards)
        y.append(y_value)

    return x, y


def save_training_data(x, y) -> None:
    with open("trainingX.txt", "w") as f:
        json.dump(x, f)
    with open("trainingY.txt", "w") as f:
        json.dump(y, f)


def load_saved_data():
    x = None
    y = None
    with open("trainingX.txt", "r") as f:
        x = json.load(f)
    with open("trainingY.txt", "r") as f:
        y = json.load(f)
    return x, y

def main():
    # x, y = get_training_data(1000000)
    # save_training_data(x, y)
    x, y = load_saved_data()
    if x and y:
        print(f"We have our training data {len(x)=}, {len(y)=}")

    x = np.array([np.array(a) for a in x])
    y = np.array([np.array(b) for b in y])
    print(x.shape, x[0].shape, y.shape, y[0].shape)


    batch_size = 128
    epochs = 15
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    model.fit(x, y, batch_size=batch_size, epochs=epochs, validation_split=0.1)

    x, y = get_training_data(1000)
    x = np.array([np.array(a) for a in x])
    y = np.array([np.array(b) for b in y])

    score = model.evaluate(x, y, verbose = 0)
    print("Test loss:", score[0])
    print("Test accuracy:", score[1])

    # Save model
    model.save('models/lowCostNN.keras')

if __name__ == "__main__":
    main()