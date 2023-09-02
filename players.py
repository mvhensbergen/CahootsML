import random


class Player:
    def __init__(self, player):
        self.player = player
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def _require_int_input(self, message):
        valid_input = True
        s = input(message)
        try:
            s = int(s)
        except:
            valid_input = False

        if not valid_input or (valid_input and (s < 0 or s > 3)):
            print("Please specify a number: 0,1,2 or 3")
            return None
        return s

    def get_move(self):
        src = None
        dest = None
        while src is None:
            src = self._require_int_input("Pick a card\n")
        while dest is None:
            dest = self._require_int_input("Place a card\n")

        return [src, dest]

    def reset(self):
        self.cards = []


class Dummy(Player):
    def get_move(self):
        return [random.randint(0, 3), random.randint(0, 3)]
