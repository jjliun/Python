#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Filename      : project6.py
# Author        : Yang Leo (JeremyRobturtle@gmail.com)
# Last Modified : 2014-05-29
'''Mini-project #6 - Blackjack
'''
import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos, back=False):
        if not back:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))

            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        else:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.masks = [False] * 5

    def __str__(self):
        return "Hand contains " + " ".join([c.suit + c.rank for c in self.cards])

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):

        ranks = [c.rank for c in self.cards]
        n_aces = ranks.count('A')
        value = sum([VALUES[r] for r in ranks])

        while n_aces > 0 and value + 10 <= 21:
            value += 10
            n_aces -= 1

        return value

    def draw(self, canvas, pos):
        x, y = pos
        offset = round(CARD_SIZE[0] * 1.2)

        for i, c in enumerate(self.cards):
            c.draw(canvas, (x + offset * i, y), self.masks[i])


# define deck class
class Deck:
    def __init__(self):
        self.cards = [Card(s, r) for s in SUITS for r in RANKS]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        try:
            return self.cards.pop()
        except IndexError:
            self.__init__()
            return self.cards.pop()

    def __str__(self):
        return "Deck contains " + " ".join([c.suit + c.rank for c in self.cards])



#define event handlers for buttons
def deal():
    global outcome, in_play
    global deck, dealer, player

    deck.shuffle()
    dealer = Hand()
    dealer.masks[0] = True
    player = Hand()

    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())

    #print "Dealer: ", dealer
    print "Player: ", player
    print deck
    print

    in_play = True

def hit():
    if not in_play:
        return

    if len(player.cards) < 5 and player.get_value() <= 21:
        player.add_card(deck.deal_card())
        print player
    else:
        print "You have busted!"

def stand():
    global in_play
    in_play = False
    dealer.masks[0] = False

    pv = player.get_value()
    if pv > 21:
        print "You have busted!"
        return

    while dealer.get_value() < 17:
        dealer.add_card(deck.deal_card())

    dv = dealer.get_value()
    if dv > 21:
        print "Dealer has busted!"
    elif dv >= pv:
        print "You lost!"
    else:
        print "You win!"

# draw handler
def draw(canvas):
    dealer.draw(canvas, [100, 200])
    player.draw(canvas, [100, 400])


# Game status
deck = Deck()

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
