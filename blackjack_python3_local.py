# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image(
    "http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image(
    "http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
          '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}

# define draw position  for player hand and dealer hand
pos_draw_player_card = [50, 400]
pos_draw_dealer_card = [50, 200]


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [
                          pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class


class Hand:
    def __init__(self):
        self.card_list = []
        pass  # create Hand object

    def __str__(self):
        cl = ""
        for card in self.card_list:
            cl += card.suit + card.rank + " "
        return "Hand contains " + cl
        pass  # return a string representation of a hand

    def add_card(self, card):
        self.card_list.append(card)
        pass  # add a card object to a hand

    def get_value(self):
        value = 0
        has_ace = 0
        for card in self.card_list:
            value += VALUES[card.rank]
            if card.rank == "A":
                has_ace += 1

        if (has_ace and (value + 10) <= 21):
            return value + 10
        else:
            return value
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        pass  # compute the value of the hand, see Blackjack video

    def draw(self, canvas, pos):
        hand_card_pos = list(pos)
        for card in self.card_list:
            card.draw(canvas, hand_card_pos)
            hand_card_pos[0] += CARD_SIZE[0] + 20
        pass  # draw a hand on the canvas, use the draw method for cards


# define deck class
class Deck:
    def __init__(self):
        self.deck = []
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s, r))

    def shuffle(self):
        random.shuffle(self.deck)
        # shuffle the deck
        pass    # use random.shuffle()

    def deal_card(self):
        return self.deck.pop()
        pass  # deal a card object from the deck

    def __str__(self):
        dl = ""
        for card in self.deck:
            dl += card.suit + card.rank + " "
        return "Deck contains " + dl
        pass  # return a string representing the deck


# define event handlers for buttons


def deal():
    global outcome, in_play
    global DEALER_HAND, PLAYER_HAND, DECK
    outcome = "hit or stand ?"
    score = 0
    DEALER_HAND = Hand()
    PLAYER_HAND = Hand()
    DECK = Deck()
    DECK.shuffle()
    PLAYER_HAND.add_card(DECK.deal_card())
    DEALER_HAND.add_card(DECK.deal_card())
    PLAYER_HAND.add_card(DECK.deal_card())

    # your code goes here

    in_play = True


def hit():
    global outcome, in_play, score
    global DEALER_HAND, PLAYER_HAND, DECK
    if in_play:
        if PLAYER_HAND.get_value() <= 21:
            PLAYER_HAND.add_card(DECK.deal_card())
        if PLAYER_HAND.get_value() >= 21:
            outcome = "You have busted"
            score -= 1
            in_play = False
    # if the hand is in play, hit the player

    # if busted, assign a message to outcome, update in_play and score


def stand():

    global outcome, in_play, score
    global DEALER_HAND, PLAYER_HAND, DECK
    if in_play:
        while DEALER_HAND.get_value() < 17 and DEALER_HAND.get_value() < PLAYER_HAND.get_value():
            DEALER_HAND.add_card(DECK.deal_card())

        if DEALER_HAND.get_value() > 21:
            outcome = "dealer has busted, you win"
            score += 1
            in_play = False
        else:
            if PLAYER_HAND.get_value() > DEALER_HAND.get_value():
                outcome = "you win"
                score += 1
                in_play = False
            else:
                outcome = "dealer win"
                score -= 1
                in_play = False
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler


def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    # draw zone promp
    global pos_draw_player_card, pos_draw_dealer_card
    canvas.draw_text("score: " + str(score), (400, 100), 40, "white")
    canvas.draw_text("Blackjack!!", [pos_draw_dealer_card[0],
                                     pos_draw_dealer_card[1] - 100], 50, "yellow")
    canvas.draw_text("Dealer's hand", [pos_draw_dealer_card[0],
                                       pos_draw_dealer_card[1] - 20], 30, "blue")
    canvas.draw_text("Plyer's hand", [pos_draw_player_card[0],
                                      pos_draw_player_card[1] - 20], 30, "blue")
    # draw outcome to the canvs
    canvas.draw_text(outcome, [pos_draw_player_card[0] + CARD_SIZE[0] * 3,
                               pos_draw_player_card[1] - 20], 30, "white")

    # draw player_card
    PLAYER_HAND.draw(canvas, pos_draw_player_card)

    # draw back of card
    pos2 = list(pos_draw_dealer_card)
    card_loc2 = CARD_BACK_CENTER
    canvas.draw_image(card_back, card_loc2, CARD_BACK_SIZE, [
        pos2[0] + CARD_BACK_CENTER[0], pos2[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

    # draw dealer_card
    pos2[0] += CARD_SIZE[0] + 20
    DEALER_HAND.draw(canvas, pos2)

    # c1 = Card("S", "3")
    # c1.draw(canvas, pos_draw_player_card)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
