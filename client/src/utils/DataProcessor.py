import subprocess
import Xlib
from Xlib import X
import hashlib


def extract_digits_from_predictions(preds) -> str:
    coords = []

    names = preds[0].names

    for cls, coord in zip(preds[0].boxes.cls, preds[0].boxes.xywh):
        coords.append([int(cls.item()), round(coord.tolist()[0], 2)])

    coords.sort(key=lambda x: x[1])

    digits = [names[item[0]] for item in coords]

    full_digit = ''.join(digits).replace('c', '.').replace('-', '.')

    return full_digit.strip('.')

def extract_card_from_predictions(preds) -> str:
    coords = []

    names = preds[0].names

    for cls, coord in zip(preds[0].boxes.cls, preds[0].boxes.xywh):
        coords.append([names[int(cls.item())], coord.tolist()[1]])

    if len(coords) < 2:
        return '-'

    coords.sort(key=lambda x: x[1])
    list_card: list = [item[0] for item in coords]
    return f'{list_card[0]} of {list_card[1]}'


def get_title():
    try:
        # Run wmctrl command to get the list of open windows
        result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True)

        # Check if the command was successful
        if result.returncode == 0:
            windows = result.stdout.splitlines()  # Split the output by newlines
            for window in windows:
                # Further processing to extract just the title
                parts = window.split(None, 3)  # Split into parts, keeping the first three
                if len(parts) >= 4:
                    title = parts[3]  # The title is the fourth part (after three spaces)
                    if "Hold'em" in title:
                        return title
        else:
            print("Error retrieving windows:", result.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")


def get_title_by_window_name(window_name) -> int:
    display = Xlib.display.Display()
    try:
        root = display.screen().root
        windowIDs = root.get_full_property(display.intern_atom('_NET_CLIENT_LIST'), X.AnyPropertyType).value

        windowID = None

        for windowID in windowIDs:
            window = display.create_resource_object('window', windowID)
            window_title_property = window.get_full_property(display.intern_atom('_NET_WM_NAME'), 0)

            if window_title_property and window_name.lower() in window_title_property.value.decode('utf-8').lower():
                return windowID

        if windowID is None:
            raise Exception('Window not found: {}'.format(window_name))
    finally:
        display.close()


def convert_string_to_hash(STR: str):
    encoded_string = STR.encode()
    hash_object = hashlib.sha256(encoded_string)
    return hash_object.hexdigest()

def sort_cards(list_of_cards: list) -> list:
    # Define the order of ranks
    rank_order = {
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
        'clubs': 1,
        'diamonds': 2,
        'hearts': 3,
        'spades': 4
    }

    if '-' in list_of_cards:
        return ['-']

    def card_sort_key(card) -> tuple:
        rank, suit = card.split(' of ')
        return rank_order[rank], suit_order[suit]

    # Sort the list of cards based on rank and suit
    return sorted(list_of_cards, key=card_sort_key)
