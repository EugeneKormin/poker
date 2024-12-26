import hashlib
import win32gui
import json

def extract_digits_from_predictions(preds) -> str:
    coords = []

    names = preds[0].names

    for cls, coord in zip(preds[0].boxes.cls, preds[0].boxes.xywh):
        coords.append([int(cls.item()), round(coord.tolist()[0], 2)])

    coords.sort(key=lambda x: x[1])

    digits = [names[item[0]] for item in coords]

    full_digit = ''.join(digits).replace('c', '.').replace('-', '.')

    return full_digit.strip('.')

def extract_card_from_predictions(preds) -> tuple:
    coords = []

    names = preds[0].names

    for cls, coord in zip(preds[0].boxes.cls, preds[0].boxes.xywh):
        coords.append([names[int(cls.item())], coord.tolist()[1]])

    # One coord might be detected if card is being rendered.
    if len(coords) < 2:
        return '-', True

    coords.sort(key=lambda x: x[1])
    list_card: list = [item[0] for item in coords]
    if list_card[0] in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'] and list_card[1] in ['clubs', 'hearts', 'spades', 'diamonds']:
        return f'{list_card[0]} of {list_card[1]}', True
    else:
        return '', False


def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        wnd_name = win32gui.GetWindowText(hwnd)
        if "Hold'em" in wnd_name:  # Check if the window title is not empty
            return ctx.append(wnd_name)

def get_title():
    window_names = []
    win32gui.EnumWindows(winEnumHandler, window_names)
    return window_names[0]


def convert_string_to_hash(STR: str):
    encoded_string = STR.encode()
    hash_object = hashlib.sha256(encoded_string)
    return hash_object.hexdigest()


def sort_cards(list_of_cards: list) -> list:
    # Define the order of ranks
    rank_order = {
        '?': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14
    }
    suit_order = {
        '?': 0,
        'clubs': 1,
        'diamonds': 2,
        'hearts': 3,
        'spades': 4
    }

    if '-' in list_of_cards:
        return ['-']

    def card_sort_key(card) -> tuple:
        rank, suit = card.split(' of ')
        if rank not in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']:
            rank = '?'
        if suit not in ['clubs', 'diamonds', 'hearts', 'spades']:
            suit = '?'
        return rank_order[rank], suit_order[suit]

    # Sort the list of cards based on rank and suit
    return sorted(list_of_cards, key=card_sort_key)

def convert_json_to_prompt(table_data: dict):
    prompt_lines = []

    # Board information
    board = table_data["board"]
    dealer_position = board["dealer_position"]
    prompt_lines.append(f"The dealer is in position {dealer_position}.")

    # Player information
    player = table_data["player"]
    player_position = player["position"]
    player_cards = ", ".join(player["cards"]) if player["cards"] else 'No cards'
    prompt_lines.append(f"You are in position {player_position} with cards: {player_cards}.")

    # Collecting information about other players at the table
    for position, info in table_data.items():
        if position not in ["board", "player", 'out_of_table', 'advice', 'action_started', 'action_ended',
                            'current_prompt_id']:
            pot = info["pot"]
            bet = info["bet"]
            in_game_status = 'in the game' if info["in_game"] else 'out of the game'

            prompt_lines.append(
                f"Player in position {position} has a pot of {pot} and a bet of {bet}, currently {in_game_status}.")

    # Additional game state information
    potential_bet = board["potential_bet"]
    actual_bet = board["actual_bet"]

    prompt_lines.append(f"The potential bet is {potential_bet} and the actual bet is {actual_bet}.")

    return "\n".join(prompt_lines)
