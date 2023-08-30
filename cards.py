import random

from colors import Color


class Card:
    def __init__(self, id, color, number):
        self.id = id
        self.color = color
        self.number = number

    def _colored(
        self,
        text,
        color_code,
    ):
        return f"\033[{color_code}m{text}\033[0m"

    def __repr__(self):
        # text = f"{self.color} - {self.number}"
        text = f"{self.number}"
        if self.color == Color.Green:
            return self._colored(text, 32)
        if self.color == Color.Pink:
            return self._colored(text, 95)
        if self.color == Color.Purple:
            return self._colored(text, 35)
        if self.color == Color.Orange:
            return self._colored(text, 33)


class CardDeck:
    def __init__(self):
        self.allcards = []
        id = 0
        for c in Color:
            for n in range(1, 8):
                for i in range(0, 2):
                    self.allcards.append(Card(id, c, n))
                id += 1
        random.shuffle(self.allcards)

    def get_cards(self):
        return self.allcards
