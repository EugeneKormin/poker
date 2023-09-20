

class Utils(object):
    def __init__(self):
        ...

    @staticmethod
    def __sort_cards(cards):
        # Define a custom sorting order for the ranks
        rank_order = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, 'T': 8, 'J': 9, 'Q': 10, 'K': 11,
                      'A': 12}

        # Sort the cards based on their rank_order
        sorted_cards = sorted(cards, key=lambda card: (rank_order.get(card[0], float('inf')), card[1]))

        return sorted_cards

    @staticmethod
    def count_suits(cards):
        # Initialize a dictionary to count the number of cards for each suit
        suit_count = {'H': 0, 'D': 0, 'C': 0, 'S': 0}

        # Count the suits in the cards
        for card in cards:
            suit = card[1]
            suit_count[suit] += 1

        return suit_count

    def analyze_cards(self, cards):
        # Sort the cards
        sorted_cards = self.__sort_cards(cards)

        # Extract the first letter of each card and create a set to ensure uniqueness
        unique_first_letters = set(card[0] for card in sorted_cards)

        return sorted_cards, unique_first_letters

    @staticmethod
    def create_straight_list():
        card_list = "AKQJT98765432"

        straight_list = []
        for index in range(len(card_list)):
            straight = card_list[index:index + 5]
            if len(straight) == 5:
                straight_list.append(straight)
            else:
                pass

        return straight_list

    @staticmethod
    def check_card(card_to_check, card_that_is_to_be_checked):
        # Define a custom sorting order for the ranks
        rank_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12,
                      'K': 13,
                      'A': 14}

        # Check if both cards are valid (e.g., not misspelled)
        if card_to_check[0] in rank_order and card_that_is_to_be_checked[0] in rank_order:
            # Compare the ranks of the two cards
            rank_card_to_check = rank_order[card_to_check[0]]
            rank_card_that_is_to_be_checked = rank_order[card_that_is_to_be_checked[0]]
            if rank_card_that_is_to_be_checked < rank_card_to_check:
                return card_to_check
            else:
                return ""

        # If any card is invalid or the card to be checked is not lower, return the card itself
        return card_that_is_to_be_checked
