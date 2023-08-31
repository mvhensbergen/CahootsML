from cards import CardDeck
from missions import MissionDeck
from visuals import Visuals


class Game:
    def __init__(self, players, number_of_missions, outdir):
        self.players = players  # Array of the players
        self.allcards = []  # The closed card deck
        self.missions = []  # The current missions
        self.solved_missions = []  # The stack of solved missions
        self.table_cards = []  # The current cards on the table
        self.played_cards = []  # The cards that have been played

        self.number_of_missions = (
            number_of_missions  # Total number of missions to solve
        )

        self.id = 0

        if outdir:
            self.v = Visuals(outdir)

    def reset(self):
        # Reset players turns and flush the played card stacks
        self.turn = 0
        self.id += 1
        self.played_cards = []
        self.solved_missions = []

        self.finished = False

        # Get a random set of mission cards
        missionsDeck = MissionDeck()
        self.allmissions = missionsDeck.get_missions(self.number_of_missions)
        self.total_possible_missions = missionsDeck.total_mission_count()

        # Get the playing cards in random order
        cardDeck = CardDeck()
        self.allcards = cardDeck.get_cards()

        # Initialize the missions
        self.missions = []
        count = self.number_of_missions
        if count > 4:
            count = 4
        for i in range(0, count):
            self.missions.append(self.allmissions.pop())

        # Deal cards on the playing deck
        self.table_cards = []
        for i in range(0, 4):
            self.table_cards.append(self.allcards.pop())

        # Deal cards to the players
        for player in self.players:
            player.reset()
            for _ in range(0, 4):
                player.add_card(self.allcards.pop())

    def get_remaining_missions(self):
        # Returns the amount of missions to play: the one on the table plus closed stack
        result = []
        for x in self.missions:
            if x:
                result.append(x)
        for x in self.allmissions:
            result.append(x)
        return result

    def get_stats(self):
        return {
            "missions_total": self.number_of_missions,
            "missions_remaining": self.get_remaining_missions(),
            "missions_solved": self.solved_missions,
            "cards_left": len(self.allcards),
            "finished": self.finished,
        }

    def get_current_player(self):
        return self.players[self.turn]

    def check_missions(self):
        # Checks all missions for completion
        fulfilled = False

        pos = 0
        while pos < len(self.missions):
            mission = self.missions[pos]
            if mission and mission.test(self.table_cards):
                # print (f"\n--> Fulfilled: {mission.desc}\n")
                fulfilled = True
                self.solved_missions.append(mission)
                if self.allmissions:
                    self.missions[pos] = self.allmissions.pop()
                else:
                    self.missions[pos] = None
            pos += 1
        return fulfilled

    def next_player(self):
        # Switch to the next player
        self.turn += 1
        self.turn = self.turn % len(self.players)

    def do_move(self, src, dest):
        # Moves a card from the players hand to the deck
        player = self.get_current_player()
        srccard = player.cards[src]

        # Add old cards to the stack of played cards
        self.played_cards.append(self.table_cards[dest])
        self.table_cards[dest] = srccard

        # If there are cards left, pick a card
        if self.allcards:
            player.cards[src] = self.allcards.pop()
        else:
            player.cards[src] = None

    def count_moves(self, player=None):
        # Count the number of valid moves for the given player
        if not player:
            player = self.get_current_player()

        count = 0
        for src in range(0, 4):
            for dest in range(0, 4):
                if self.valid_move(src, dest, player):
                    count += 1
        return count

    def valid_move(self, src, dest, player=None):
        # Check if a move is valid
        if not player:
            player = self.get_current_player()

        srccard = player.cards[src]
        if not srccard:
            return False

        dstcard = self.table_cards[dest]
        if srccard.color == dstcard.color:
            return True
        if srccard.number == dstcard.number:
            return True
        return False

    def finish_turn(self, first_time=False, valid_move=True):
        # Checks for solved missions and if the game has ended
        # Note that it is possible to solve multiple missions at once

        solved_mission = True  # Whether or not a mission was finished
        solved_mission_count = 0  # Total number of missions finished in this round

        while solved_mission:
            solved_mission = self.check_missions()
            if solved_mission:
                solved_mission_count += 1

        # Check if we have won the game
        if len(self.allmissions) == 0 and len(self.get_remaining_missions()) == 0:
            self.finished = True
            return solved_mission_count

        # Check if there are still possible moves
        total_moves = 0
        for player in self.players:
            # print (f"{player.player} has {self.count_moves(player)} moves")
            total_moves += self.count_moves(player)

        if total_moves == 0:
            # print ("No valid moves... game over")
            self.finished = True
            return solved_mission_count

        # Determine the next player
        # At the beginning of the game, if a mission is solved by coincedence, don't
        # switch to next player
        if valid_move and solved_mission_count == 0 and not first_time:
            self.next_player()

        return solved_mission_count

    def get_player_action(self):
        # Ask the Player class for an action
        player = self.get_current_player()
        [src, dest] = player.get_move()
        return [src, dest]

    def visual_render(self):
        self.v.render_missions(self.missions)
        for i, c in enumerate(self.table_cards):
            self.v.render_deck_card(i, c.color, c.number)
        for i, c in enumerate(self.get_current_player().cards):
            if c:
                self.v.render_player_card(i, c.color, c.number)

        description = (
            f"{self.get_current_player().player} - Ep: {self.id} - Cards left: {len(self.allcards)} "
            f"- Missions left:{len(self.get_remaining_missions())}"
        )
        self.v.render_description(description)
        self.v.draw()

    def print(self, extended=True):
        self.visual_render()

        print(
            f"*** Missions left: {len(self.allmissions)} *** Cards left: {len(self.allcards)} ***"
        )
        print("Current Missions:")
        for m in self.missions:
            if m:
                print(f"- {m}")
            else:
                print("- ------")

        print()

        player = self.get_current_player()

        print("# - P - D")
        for i in range(0, 4):
            print(f"{i} - {player.cards[i]} - {self.table_cards[i]}")

        print()

        if extended:
            print("Played cards:", self.played_cards)
            print("Played missions:", self.solved_missions)

        print()
        print(f"It's Player {player.player}'s turn")
        return
