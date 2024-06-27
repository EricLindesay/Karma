import Deck, random
from multipledispatch import dispatch
from config import ALWAYS_PLAYABLE_CARDS
from collections import Counter
from Player import Player


class RandomPlayer(Player):

    def choose_cards(self, playable_cards: list[int]) -> int:
        c = Counter(playable_cards)
        card = random.choice(playable_cards)

        return (card, c[card])

