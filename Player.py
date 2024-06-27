import Deck, random
from multipledispatch import dispatch
from config import ALWAYS_PLAYABLE_CARDS
from collections import Counter


class Player:
    hand: list[int] = []
    up_cards: list[int] = []
    down_cards: list[int] = []  # The user should never be able to see this
                                # Maybe store it somewhere else?
    i = 0

    def __init__(self, i: int):
        self.hand = []
        self.up_cards = []
        self.down_cards = []
        self.i = i
    
    def init_add_card(self, card: int):
        if len(self.down_cards) < 3:
            self.down_cards.append(card)
            return
        if len(self.up_cards) < 3:
            self.up_cards.append(card)
            return
        else:
            self.hand.append(card)

    def swap_face_up(self) -> None:
        # Swap your best cards in hand with the face up cards
        cards = self.hand
        cards.extend(self.up_cards)
        # Find the best three of these

        special = [x for x in cards if x in ALWAYS_PLAYABLE_CARDS]
        special.sort()
        c1 = Counter(cards)
        c2 = Counter(special)
        diff = c1 - c2
        non_special = list(diff.elements())
        non_special.sort()
        
        self.up_cards = []
        while len(self.up_cards) < 3:
            if len(special) > 0:
                self.up_cards.append(special[-1])
                del special[-1]
            else:
                self.up_cards.append(non_special[-1])
                del non_special[-1]

        c1 = Counter(cards)
        c2 = Counter(self.up_cards)
        diff = c1 - c2
        self.hand = list(diff.elements())

    @dispatch(object, int)
    def add_to_hand(self, card: int) -> None:
        self.hand.append(card)

    @dispatch(object, list)
    def add_to_hand(self, cards: list[int]) -> None:
        self.hand.extend(cards)

    def play(self) -> None:
        self.play_card()
    
        while len(self.hand) < 3 and Deck.can_draw():
            self.draw_card()

    def get_playable_cards(self) -> list[int]:
        if len(self.hand) > 0:
            # Play your hand if you can
            playable_cards = [card for card in self.hand if Deck.can_play_card(card)]
            source = self.hand
        elif len(self.up_cards) > 0:
            # You have no hand, play the face up cards
            playable_cards = [card for card in self.up_cards if Deck.can_play_card(card)]
            source = self.up_cards
        elif len(self.down_cards) > 0:
            # Play a random down card
            source = None

            card = random.choice(self.down_cards)
            for i in range(len(self.down_cards)):
                if self.down_cards[i] == card:
                    del self.down_cards[i]
                    break

            if Deck.can_play_card(card):
                playable_cards = [card]
            else:
                playable_cards = []
                self.hand.append(card)
        else:
            return None, None

        return playable_cards, source

    def play_card(self):
        playable_cards, source = self.get_playable_cards()
        if playable_cards == None:
            return
        
        self.play_from_hand(playable_cards, source)

    def play_from_hand(self, playable_cards, source):
        # If there are no playable cards, pickup
        if len(playable_cards) == 0:
            self.pickup_pile()
            return

        # Get the card
        card, num = self.choose_cards(playable_cards)
        n = num
        # Remove `num` instances of the card from hand
        if source:
            for i in range(len(source)-1, -1, -1):
                if source[i] == card:
                    del source[i]
                    num -= 1
                    if num == 0:
                        break
        
        # Play that card
        play_again = Deck.play_card(card, n)
        print(f"Player {self.i} plays a {card} card, {n} times")
        if play_again:
            self.play_card()

    def choose_cards(self, playable_cards: list[int]) -> tuple[int]:
        raise NotImplementedError(f"{self.__class__}.choose_cards() has not been implemented")

    def draw_card(self):
        card = Deck.draw_card()            
        self.hand.append(card)

    def pickup_pile(self):
        self.hand.extend(Deck.pile)
        print(f"{self.i} picked up so now we have: {self.hand}")
        Deck.clear_pile()

    def finished(self):
        return len(self.hand) == 0 and len(self.up_cards) == 0 and len(self.down_cards) == 0
    
    def __str__(self):
        return f"{self.__class__} {self.i} has hand {self.hand} and up {self.up_cards} and down {self.down_cards}"