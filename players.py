import random


class Player:
    def __init__(self, player):
        self.player = player
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_move(self):
        src = int(input("Pick a card\n"))
        dest = int(input("Place card\n"))
        return [src, dest]

    def reset(self):
        self.cards = []


class Dummy(Player):
    def get_move(self):
        return [random.randint(0, 3), random.randint(0, 3)]
