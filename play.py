from cahoots import Game
from players import Dummy, Player

players = [
    Player("You"),
    Dummy("Computer"),
]

g = Game(players=players, number_of_missions=4, outdir=None)
g.reset()

g.finish_turn(first_time=True)

won = 0
lost = 0
iter = 0

# Actions = [ Pij -> Cmn ]

while True:
    # GAME
    g.print()

    if g.count_moves() == 0:
        print("NO AVAILABLE MOVES")
        g.finish_turn()

    else:
        src, dest = g.get_player_action()

        if not g.valid_move(src, dest):
            print("*** Invalid Move ***")
            g.finish_turn(valid_move=False)  # Do not switch the turn
        else:
            g.do_move(src, dest)
            g.finish_turn()

    # Meta
    state = g.get_stats()
    if state["finished"]:
        iter += 1
        if len(state["missions_remaining"]) == 0:
            won += 1
            print("WON!")
        else:
            lost += 1
            print("LOST!")
        print(f"Solved missions    : {state['missions_solved']}")
        print(f"Remaining missions : {state['missions_remaining']}")

        # print(g.played_cards)
        # for c in g.played_cards:
        # 	print(c.encode(), end=" ")

        # input("Continue?")

        g.reset()
        g.finish_turn(first_time=True)

        if iter % 100 == 0:
            print(f"Iter/Won/Lost: {iter}/{won}/{lost}")
