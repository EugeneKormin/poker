from Outs import Outs


outs = Outs()

player_hand_cards = ["3H", "5H"]
board_cards = ["QH", "6H", "4H"]

if __name__ == "__main__":
    outs.set_player_hand(player_hand=player_hand_cards)
    outs.set_board(board=board_cards)

    outs, combination = outs.get()
    print(outs)
