import random
import copy


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

    def get_move(self, g):
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
    def get_move(self, g):
        return [random.randint(0, 3), random.randint(0, 3)]


class MissionMinded(Player):
    def _backup_state(self, g):
        self.players = copy.deepcopy(g.players)
        self.allcards = copy.deepcopy(g.allcards)
        self.missions = copy.deepcopy(g.missions)
        self.solved_missions = copy.deepcopy(g.solved_missions)
        self.table_cards = copy.deepcopy(g.table_cards)
        self.played_cards = copy.deepcopy(g.played_cards)

        self.finished = copy.deepcopy(g.finished)
        self.turn = copy.deepcopy(g.turn)

    def _restore_state(self, g):
        g.players = copy.deepcopy(self.players)
        g.allcards = copy.deepcopy(self.allcards)
        g.missions = copy.deepcopy(self.missions)
        g.solved_missions = copy.deepcopy(self.solved_missions)
        g.table_cards = copy.deepcopy(self.table_cards)
        g.played_cards = copy.deepcopy(self.played_cards)

        g.finished = copy.deepcopy(self.finished)
        g.turn = copy.deepcopy(self.turn)

    def get_move(self, g):
        valid_moves = []
        best_move = None

        ## Bakcup state
        self._backup_state(g)

        # Restore state

        last_count = -1
        for src in range(0, 4):
            for dest in range(0, 4):
                # Copy the current state of the game

                self._restore_state(g)

                if not g.valid_move(src, dest):
                    print(f"Invalid move {src} -> {dest}")
                    continue
                print(f"Trying move {src} -> {dest}")

                valid_moves.append([src, dest])

                g.do_move(src, dest)

                count = g.finish_turn()

                if count > last_count:
                    best_move = [src, dest]

                last_count = count

                print(f"{src}->{dest} would sovle {count} missions")

        self._restore_state(g)
        if best_move:
            print(f"Playing: {best_move}")
            return best_move
        return random.choice(valid_moves)
