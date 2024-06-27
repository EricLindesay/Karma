import Deck, random
from multipledispatch import dispatch
from config import ALWAYS_PLAYABLE_CARDS
from collections import Counter
from Player import Player


class LowCardPlayer(Player):

    def choose_cards(self, playable_cards: list[int]) -> tuple[int]:
        # Extract sepcial and non-special
        special = [x for x in playable_cards if x in ALWAYS_PLAYABLE_CARDS]
        non_special = [x for x in playable_cards if x not in ALWAYS_PLAYABLE_CARDS]

        non_special.sort()
        special.sort()

        if len(non_special) > 0:
            num = 0
            for c in non_special:
                if c != non_special[0]:
                    break
                num += 1
            # Play as many non-special cards as you can
            return (non_special[0], num)
        elif len(special) > 0:
            # Always play one special card
            return (special[0], 1)
        else:
            raise ValueError("Playable cards must be non-empty")