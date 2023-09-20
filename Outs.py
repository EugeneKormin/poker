from collections import Counter
from Utils import Utils


class Outs(object):
    def __init__(self):
        self.__utils = Utils()
        self.__straight_list = self.__utils.create_straight_list()
        self.__player_hand = []
        self.__board = []
        
    def set_player_hand(self, player_hand):
        self.__player_hand = player_hand
        
    def set_board(self, board):
        self.__board = board
        
    def get(self):
        self.__calculate()
        return self.__outs, self.__combination
        
    def __calculate(self):
        self.__check_for_royal_flush()
        self.__check_for_straight_flush()
        self.__check_for_four_of_a_kind()
        self.__check_for_full_house()
        self.__check_for_flush()
        self.__check_for_straight_flush()

    def __check_for_royal_flush(self):
        # Combine the player's hand and board cards into a single list
        all_cards = self.__player_hand + self.__board
        straight_list = self.__straight_list

        cards = []
        self.__outs = []
        self.__combination = ""
        for suit in ["C", "H", "D", "S"]:
            check_sum = 0
            for card in all_cards:
                if card[0] in straight_list[0] and suit == card[1]:
                    check_sum += 1
                    cards.append(card[0])

            res_list = list(straight_list[0])
            if 5 - check_sum == 0:
                self.__combination = "flush_royal"
            elif 5 - check_sum == 1:
                for card in cards:
                    res_list.remove(card)
                self.__outs += [hand + suit for hand in res_list]
            else:
                self.__outs += []

    def __check_for_straight_flush(self):
        # Combine the player's hand and board cards into a single list
        all_cards = self.__player_hand + self.__board
        straight_list = self.__straight_list
    
        cards = []
        self.__outs = []
        self.__combination = ""
        check_sum = 0
        for suit in ["C", "H", "D", "S"]:
    
            for a_straight in straight_list:
                for card in all_cards:
                    if card[0] in a_straight and suit == card[1]:
                        if card[0] not in cards:
                            check_sum += 1
                            cards.append(card[0])
                if check_sum > 3:
                    res_list = list(straight_list[0])
                    if 5 - check_sum == 0:
                        self.__combination = "straight_flush"
                    elif 5 - check_sum == 1:
                        for card in cards:
                            if card in res_list:
                                res_list.remove(card)
                        self.__outs += [hand + suit for hand in res_list]
                    else:
                        self.__outs += []
                check_sum = 0
    
        self.__outs = list(set(self.__outs))

    def __check_for_four_of_a_kind(self):
        # Combine the player's hand and board cards into a single list
        all_cards = self.__player_hand + self.__board

        # Analyze the cards
        sorted_all_cards = self.__utils.analyze_cards(all_cards)
        first_letters = [card[0] for card in sorted_all_cards]
        letter_count = {letter: first_letters.count(letter) for letter in set(first_letters)}

        most_frequent_letter = max(letter_count, key=lambda letter: letter_count[letter])
        suit_list = ["C", "H", "D", "S"]
        self.__combination = ""
        self.__outs = []
        if 3 in letter_count.values():
            for card in sorted_all_cards:
                if most_frequent_letter in card:
                    suit_list.remove(card[1])
                    self.__outs = suit_list
            self.__out = [most_frequent_letter + self.__outs[0]]
        elif 4 in letter_count.values():
            self.__combination = "four_of_a_kind"
            self.__out = []
        else:
            self.__combination = ""
            self.__out = []

    def __check_for_full_house(self):
        cards = []
        self.__outs = []
        self.__combination = ""
        check_1 = check_2 = False

        # Combine the player's hand and board cards into a single list
        all_cards = self.__player_hand + self.__board
        ranks = [card[0] for card in all_cards]

        element_count = Counter(ranks)
        # Print the element counts
        for element, count in element_count.items():
            if count > 1:
                check_1 = True
                cards.append(element)
            if count > 2:
                check_2 = True

        if check_1 and check_2:
            self.__combination = "full_house"
        else:
            for suit in ["C", "H", "D", "S"]:
                self.__outs += [hand + suit for hand in cards]

    def __check_for_flush(self):
        # Combine the player's hand and board cards into a single list
        all_cards = self.__player_hand + self.__board
        self.__combination = ""
        self.__outs = []
    
        suit_list = ["C", "H", "D", "S"]
        for suit in suit_list:
            check = 0
            for card in all_cards:
                if suit in card:
                    check += 1
            if check == 4:
                card_list = "AKQJT98765432"
                for rank in card_list:
                    self.__outs.append(rank + suit)
            elif check == 5:
                self.__combination = "flush"
                self.__outs = []

    def __check_for_straight(self):
        # Combine the player's hand and board cards into a single list
        all_cards = self.__player_hand + self.__board

        # Analyze the cards
        sorted_all_cards, unique_first_letters = self.__utils.analyze_cards(all_cards)

        unique_first_letters = ''.join(unique_first_letters)
        straight_list = self.__straight_list()

        self.__outs = []
        self.__combination = ""
        for check_straight in straight_list:
            check_sum = 0
            cards = []
            for card in unique_first_letters:
                if card in check_straight:
                    check_sum += 1
                    if card not in cards:
                        cards.append(card)

            res_list = list(check_straight)
            if 5 - check_sum == 1:
                for card in cards:
                    res_list.remove(card)
                self.__outs += res_list
            if 5 - check_sum == 0:
                straight_flush_high_card = check_straight[0]
                self.__combination = f"straight_flush_from_{straight_flush_high_card}"

        poker_hands_with_suits = []
        for suit in ["C", "H", "D", "S"]:
            poker_hands_with_suits += [hand + suit for hand in self.__outs]

        straight_flush_high_card = ""

        if self.__combination != "":
            actual_out_list = []
            for card in poker_hands_with_suits:
                actual_out = self.__utils.check_card(card[0], straight_flush_high_card)
                if len(actual_out) > 0:
                    for suit in ["C", "H", "D", "S"]:
                        actual_out_list += [actual_out + suit]
                    break

            self.__outs = actual_out_list
