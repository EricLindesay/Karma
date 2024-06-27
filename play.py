from Player import Player
from RandomPlayer import RandomPlayer
from LowCardPlayer import LowCardPlayer
from LowCostNNPlayer import LowCostNNPlayer
import Deck
from config import PLAYERS


players: list[Player] = []

def deal_cards():
    for i in range(9):  # Each player gets 9 cards to start with
        print(len(Deck.deck))
        for player in players:
            player.init_add_card(Deck.draw_card())

def main():
    for i in range(PLAYERS):
        players.append(LowCostNNPlayer(i))

    Deck.init_deck()

    deal_cards()
    print("\nDealt cards, now start swapping\n")
    for player in players:
        player.swap_face_up()
        print(player)
    
    print("\nAll players have swapped, start playing\n")
    while True:
        for player in players:
            print(f"Pile: {Deck.pile}")
            player.play()
            print(player)
            if player.finished():
                print(f"Player {player.i} won!")
                return

if __name__ == "__main__":
    main()