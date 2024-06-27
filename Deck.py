from config import RESET_CARD, BURN_CARD, LOWER_CARD, INVISIBLE_CARD, ALWAYS_PLAYABLE_CARDS
import random


deck: list[int] = []  # Cards which are in the deck
burnt: list[int] = []  # Cards taken out of play which will never be used again

pile: list[int] = []  # Cards in the pile


def init_deck() -> int:
    global deck, burnt, pile
    deck = []
    burnt = []
    pile = []

    for i in range(2, 15):  # Ace = 14
        deck.append(i)
        deck.append(i)
        deck.append(i)
        deck.append(i)

   
def get_current_card() -> int:
    if len(pile) == 0:
        return 0
    
    for i in range(len(pile)-1, -1, -1):
        # If theres an invisible card, play as if it isn't there 
        if pile[i] != INVISIBLE_CARD:
            return pile[i]
        
    return 0


def can_play_card(card: int) -> bool:
    card_to_beat = get_current_card()

    # If they played the lower card and your card is lower, good
    if card_to_beat == LOWER_CARD and card <= card_to_beat:
        return True
    
    # Can your card beat the current card?
    if card_to_beat != LOWER_CARD and card >= card_to_beat:
        return True
    
    # Is it a special card?
    if card in ALWAYS_PLAYABLE_CARDS:
        return True

    return False


def play_card(card: int, amount: int = 1) -> bool:  # Returns whether they can play another card
    global pile

    # Assume the card they are playing has already been sanitised
    for i in range(amount):
        pile.append(card)

    # If they play the burn card of if four of the same cards
    # are played in a row, burn the deck
    if card == BURN_CARD or (len(pile) >= 4 and all(i == card for i in pile[-4:])):
        burnt.extend(pile)
        pile = []
        return True
    
    return False


def draw_card() -> int:
    card = random.choice(deck)
    # Remove the card from the deck
    for i in range(len(deck)):
        if deck[i] == card:
            del deck[i]
            break

    print(deck)
    return card


def can_draw() -> bool:
    return len(deck) > 0


def clear_pile() -> None:
    pile.clear()