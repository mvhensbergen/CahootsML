import random
from colors import Color


def is_even(v):
    return v % 2 == 0


def sum_color(color, cards):
    sum = 0
    for card in cards:
        if card.color == color:
            sum += card.number
    return sum


def sum_all(cards):
    sum = 0
    for card in cards:
        sum += card.number
    return sum


def get_positions(color, cards):
    arr = []
    for index, card in enumerate(cards):
        if card.color == color:
            arr.append(index)
    return arr


def get_values(cards):
    values = []
    for card in cards:
        values.append(card.number)
    return list(set(values))


def get_colors(cards):
    colors = []
    for card in cards:
        colors.append(card.color)
    return list(set(colors))


class MissionDeck:
    def __init__(self):
        self.allmissions = create_missions()
        id = 0
        for m in self.allmissions:
            m.id = id
            id += 1
        random.shuffle(self.allmissions)

    def get_missions(self, n):
        return self.allmissions[0:n]

    def total_mission_count(self):
        return len(self.allmissions)


class MissionFactory:
    @classmethod
    def create_sum_mission(cls):
        class Mission:
            def __init__(self, color, amount):
                self.color = color
                self.amount = amount

            def test(self, cards):
                return sum_color(self.color, cards) == self.amount

            def __repr__(self):
                return f"Sum of {self.color} is {self.amount}"

        return Mission

    @classmethod
    def create_total_mission(cls):
        class Mission:
            def __init__(self, amount):
                self.amount = amount

            def test(self, cards):
                return sum_all(cards) == self.amount

            def __repr__(self):
                return f"Sum of all is {self.amount}"

        return Mission

    @classmethod
    def create_halfsum_mission(cls):
        class Mission:
            def __init__(self, color1, color2):
                self.color1 = color1
                self.color2 = color2

            def test(self, cards):
                sum1 = sum_color(self.color1, cards)
                sum2 = sum_color(self.color2, cards)
                if sum1 * sum2 == 0:
                    return False
                return sum1 == sum2 / 2

            def __repr__(self):
                return f"Sum of {self.color1} is half the sum of {self.color2}"

        return Mission

    @classmethod
    def create_equalsum_mission(cls):
        class Mission:
            def __init__(self, color1, color2):
                self.color1 = color1
                self.color2 = color2

            def test(self, cards):
                sum1 = sum_color(self.color1, cards)
                sum2 = sum_color(self.color2, cards)
                if sum1 * sum2 == 0:
                    return False
                return sum1 == sum2

            def __repr__(self):
                return f"Sum of {self.color1} is the sum of {self.color2}"

        return Mission

    @classmethod
    def create_two_adjacent_mission(cls):
        class Mission:
            def __init__(self, color):
                self.color = color

            def test(self, cards):
                positions = get_positions(self.color, cards)
                if len(positions) != 2:
                    return False
                pos1 = positions[0]
                pos2 = positions[1]
                if abs(pos1 - pos2) == 1:
                    return True
                return False

            def __repr__(self):
                return f"Two {self.color} next to eachother"

        return Mission

    @classmethod
    def create_two_non_adjacent_mission(cls):
        class Mission:
            def __init__(self, color):
                self.color = color

            def test(self, cards):
                positions = get_positions(self.color, cards)
                if len(positions) != 2:
                    return False
                pos1 = positions[0]
                pos2 = positions[1]
                if abs(pos1 - pos2) > 1:
                    return True
                return False

            def __repr__(self):
                return f"Two {self.color} not next to eachother"

        return Mission

    @classmethod
    def create_two_colors_mission(cls):
        class Mission:
            def __init__(self, color1, color2):
                self.color1 = color1
                self.color2 = color2

            def test(self, cards):
                positions1 = get_positions(self.color1, cards)
                positions2 = get_positions(self.color2, cards)
                return len(positions1) + len(positions2) == 4

            def __repr__(self):
                return f"All cards are {self.color1} or {self.color2}"

        return Mission

    @classmethod
    def create_one_and_three_or_two_and_four_mission(cls):
        class Mission:
            def __init__(self, color):
                self.color = color

            def test(self, cards):
                positions = get_positions(self.color, cards)
                if len(positions) != 2:
                    return False
                if positions == [1, 3] or positions == [2, 4]:
                    return True
                return False

            def __repr__(self):
                return f"Only 1 & 3 or 2 & 4 are {self.color}"

        return Mission

    @classmethod
    def create_three_of_color_mission(cls):
        class Mission:
            def __init__(self, color):
                self.color = color

            def test(self, cards):
                positions = get_positions(self.color, cards)
                if len(positions) == 3:
                    return True
                return False

            def __repr__(self):
                return f"Three {self.color} cards"

        return Mission

    @classmethod
    def create_more_or_less_than_four_mission(cls):
        class Mission:
            def __init__(self, sign):
                self.sign = sign  # 0 = <, 1 = >

            def test(self, cards):
                for card in cards:
                    if self.sign == 0:
                        if not card.number < 4:
                            return False
                    if self.sign == 1:
                        if not card.number > 4:
                            return False
                return True

            def __repr__(self):
                if self.sign == 0:
                    return "All numbers are less than 4"
                return "All numbers are greater than 4"

        return Mission

    @classmethod
    def create_sameness_mission(cls):
        class Mission:
            def __init__(self, mode):
                self.mode = mode

            def test(self, cards):
                if self.mode == 0:
                    values = get_values(cards)
                    return len(values) == 1
                if self.mode == 1:
                    values = get_values(cards)
                    return len(values) == 4
                if self.mode == 2:
                    values = get_values(cards)
                    colors = get_colors(cards)
                    return len(values) == 4 and len(colors) == 4
                if self.mode == 3:
                    colors = get_colors(cards)
                    return len(colors) == 4

            def __repr__(self):
                if self.mode == 0:
                    return "All cards have same number"
                if self.mode == 1:
                    return "All cards have different numbers"
                if self.mode == 2:
                    return "All cards have different numbers and colors"
                if self.mode == 3:
                    return "All cards have different colors"

        return Mission

    @classmethod
    def create_oddness_mission(cls):
        class Mission:
            def __init__(self, mode):
                self.mode = mode

            def test(self, cards):
                if self.mode == 0:
                    if is_even(cards[0].number) and is_even(cards[2].number):
                        if not is_even(cards[1].number) and not is_even(
                            cards[3].number
                        ):
                            return True
                    if not is_even(cards[0].number) and not is_even(cards[2].number):
                        if is_even(cards[1].number) and is_even(cards[3].number):
                            return True
                    return False

                else:
                    for card in cards:
                        if self.mode == 1:
                            if not is_even(card.number):
                                return False
                        if self.mode == 2:
                            if is_even(card.number):
                                return False
                    return True

            def __repr__(self):
                if self.mode == 0:
                    return "Alternating even and uneven or vice versa"
                if self.mode == 1:
                    return "All numbers are even"
                if self.mode == 2:
                    return "All numbers are odd"

        return Mission

    @classmethod
    def create_sequence_mission(cls):
        class Mission:
            def __init__(self, mode):
                self.mode = mode

            def test(self, cards):
                if self.mode == 0:
                    if (
                        cards[0].number == cards[1].number - 1
                        and cards[1].number == cards[2].number - 1
                    ):
                        return True
                    if (
                        cards[1].number == cards[2].number - 1
                        and cards[2].number == cards[3].number - 1
                    ):
                        return True
                    return False
                if self.mode == 1:
                    values = get_values(cards)
                    values.sort()
                    if len(values) != 4:
                        return False
                    if values[0] == values[3] - 3:
                        return True
                    return False

            def __repr__(self):
                if self.mode == 0:
                    return "Three ascending numbers"
                if self.mode == 1:
                    return "Four ascending numbers in random order"

        return Mission


def create_missions():
    missions = []

    factory = MissionFactory.create_sum_mission()
    missions.append(factory(Color.Pink, 10))
    missions.append(factory(Color.Green, 6))
    missions.append(factory(Color.Orange, 11))
    missions.append(factory(Color.Orange, 9))
    missions.append(factory(Color.Orange, 2))
    missions.append(factory(Color.Purple, 3))
    missions.append(factory(Color.Pink, 6))
    missions.append(factory(Color.Pink, 4))
    missions.append(factory(Color.Purple, 9))
    missions.append(factory(Color.Green, 7))
    missions.append(factory(Color.Green, 2))

    factory = MissionFactory.create_total_mission()
    missions.append(factory(10))
    missions.append(factory(15))
    missions.append(factory(18))
    missions.append(factory(20))

    factory = MissionFactory.create_halfsum_mission()
    missions.append(factory(Color.Pink, Color.Purple))
    missions.append(factory(Color.Green, Color.Orange))
    missions.append(factory(Color.Purple, Color.Green))
    missions.append(factory(Color.Orange, Color.Pink))

    factory = MissionFactory.create_equalsum_mission()
    missions.append(factory(Color.Pink, Color.Orange))
    missions.append(factory(Color.Orange, Color.Green))
    missions.append(factory(Color.Purple, Color.Pink))
    missions.append(factory(Color.Green, Color.Purple))

    factory = MissionFactory.create_two_adjacent_mission()
    missions.append(factory(Color.Pink))
    missions.append(factory(Color.Orange))
    missions.append(factory(Color.Purple))
    missions.append(factory(Color.Green))

    factory = MissionFactory.create_two_non_adjacent_mission()
    missions.append(factory(Color.Pink))
    missions.append(factory(Color.Orange))
    missions.append(factory(Color.Purple))
    missions.append(factory(Color.Green))

    factory = MissionFactory.create_two_colors_mission()
    missions.append(factory(Color.Green, Color.Pink))
    missions.append(factory(Color.Pink, Color.Purple))
    missions.append(factory(Color.Purple, Color.Orange))
    missions.append(factory(Color.Green, Color.Orange))

    factory = MissionFactory.create_one_and_three_or_two_and_four_mission()
    missions.append(factory(Color.Pink))
    missions.append(factory(Color.Green))
    missions.append(factory(Color.Orange))
    missions.append(factory(Color.Purple))

    factory = MissionFactory.create_three_of_color_mission()
    missions.append(factory(Color.Pink))
    missions.append(factory(Color.Green))
    missions.append(factory(Color.Orange))
    missions.append(factory(Color.Purple))

    factory = MissionFactory.create_more_or_less_than_four_mission()
    missions.append(factory(0))
    missions.append(factory(1))

    factory = MissionFactory.create_sameness_mission()
    missions.append(factory(0))
    missions.append(factory(1))
    missions.append(factory(2))
    missions.append(factory(3))

    factory = MissionFactory.create_oddness_mission()
    missions.append(factory(0))
    missions.append(factory(1))
    missions.append(factory(2))

    factory = MissionFactory.create_sequence_mission()
    missions.append(factory(0))
    missions.append(factory(1))

    assert len(missions) == 54
    return missions
