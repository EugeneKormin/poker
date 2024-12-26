from client.src.core.PokerTableDistributor import PokerTableDistributor
from client.src.core.Predictor import Predictor
from client.src.utils.DataProcessor import extract_digits_from_predictions, extract_card_from_predictions, sort_cards
from client.src.utils.ScreenCapture import ScreenCapture

import random
import redis
import json

screen_capture = ScreenCapture()
poker_table_distributor = PokerTableDistributor()


class PokerDataParser(object):
    def __init__(self, config: dict):
        REDIS_HOST: str = config['server']['url']
        REDIS_PORT: str = config['server']['redis_port']
        self.client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        self.__PLAYER_CARDS = []

    def __update(self, PLAYER_QUANTITY: int):

        self.__hand_count = 0
        self.__action_count = 1

        if PLAYER_QUANTITY == 6:
            self.__overall = {
                'out_of_table': {},
                1: {'pot': '-', 'bet': '-', 'cards': [], 'in_game': False},
                2: {'pot': '-', 'bet': '-', 'cards': [], 'in_game': False},
                3: {'pot': '-', 'bet': '-', 'cards': [], 'in_game': False},
                4: {'pot': '-', 'bet': '-', 'cards': [], 'in_game': False},
                5: {'pot': '-', 'bet': '-', 'cards': [], 'in_game': False},
                6: {'pot': '-', 'bet': '-', 'cards': [], 'in_game': False},
                'board': {'dealer_position': '-', 'cards': [], 'potential_bet': '0', 'actual_bet': '0', 'hand_id': ''},
                'player': {'cards': [], 'pot': '-', 'bet': '-', 'call': 0, 'position': '-', 'action': False, 'action_counter': 0},
                'advice': ''
            }

        if PLAYER_QUANTITY == 8:
            self.__overall = {
                'out_of_table': {},
                1: {'pot': '-', 'bet': '-', 'in_game': False},
                2: {'pot': '-', 'bet': '-', 'in_game': False},
                3: {'pot': '-', 'bet': '-', 'in_game': False},
                4: {'pot': '-', 'bet': '-', 'in_game': False},
                5: {'pot': '-', 'bet': '-', 'in_game': False},
                6: {'pot': '-', 'bet': '-', 'in_game': False},
                7: {'pot': '-', 'bet': '-', 'in_game': False},
                8: {'pot': '-', 'bet': '-', 'in_game': False},
                'board': {'dealer_position': '-', 'cards': [], 'potential_bet': '0', 'actual_bet': '0', 'hand_id': ''},
                'player': {'cards': [], 'pot': '-', 'bet': '-', 'call': 0, 'position': '-', 'action': False, 'action_counter': 0},
                'advice': ''
            }

    def __convert_bet_coords_to_digit_prediction(self, config,  coords, roi, MODEL_TYPE: str):
        BELONGS_TO = poker_table_distributor.distribute_bets(config=config, coords=coords)

        try:
            preds = self.__predict.run(MODEL_TYPE=MODEL_TYPE, image=roi)
            DIGIT = extract_digits_from_predictions(preds=preds).replace('..', '.')
            try:
                float(DIGIT)
            except ValueError:
                DIGIT = '-'
            return BELONGS_TO, DIGIT
        except:
            return '-', 0

    def __convert_player_poker_coords_to_digit_prediction(self, config,  coords, roi, MODEL_TYPE: str):
        BELONGS_TO = poker_table_distributor.distribute_player_pots(config=config, coords=coords)

        try:
            preds = self.__predict.run(MODEL_TYPE=MODEL_TYPE, image=roi)
            DIGIT = extract_digits_from_predictions(preds=preds)
            return BELONGS_TO, DIGIT
        except:
            return '-', 0

    def __convert_board_bet_coords_to_digit_prediction(self, roi, MODEL_TYPE: str):
        try:
            preds = self.__predict.run(MODEL_TYPE=MODEL_TYPE, image=roi)
            DIGIT = extract_digits_from_predictions(preds=preds)
            return DIGIT
        except:
            return '-', 0

    def __convert_coords_to_card_prediction(self, coords, roi):
        BELONGS_TO = poker_table_distributor.distribute_cards(coords=coords)
        
        preds = self.__predict.run(image=roi)
        
        CARD, PRED_CHECK = extract_card_from_predictions(preds=preds)

        return BELONGS_TO, CARD, PRED_CHECK

    def __convert_coords_to_player_position(self, config,  coords) -> str:
        BELONGS_TO = str(poker_table_distributor.distributed_cards2player_position(config=config, coords=coords))
        return BELONGS_TO

    def __convert_coords_to_dealer_position(self, config, coords) -> str:
        BELONGS_TO = poker_table_distributor.distributed_cards2dealer_position(config=config, coords=coords)
        return BELONGS_TO

    def __parse(self, IDX, name, coords, screenshot, config):
        self.__predict = Predictor(config=config)
        CENTER_X = int(coords[0] + int(coords[2])) // 2
        CENTER_Y = int(coords[1] + int(coords[3])) // 2

        if name == 'bet' and len(coords) > 0:
            roi = screenshot[CENTER_Y-16:CENTER_Y+16, CENTER_X-48:CENTER_X+48]

            BELONGS_TO, DIGIT = self.__convert_bet_coords_to_digit_prediction(config=config, coords=coords, roi=roi, MODEL_TYPE='bet_detector')

            if BELONGS_TO != 0:
                self.__overall[BELONGS_TO]['bet'] = str(DIGIT)
            else:
                self.__overall['out_of_table'] = None

        elif name == 'player-pot' and len(coords) > 0:
            roi = screenshot[CENTER_Y-16:CENTER_Y+16, CENTER_X-80:CENTER_X+80]

            BELONGS_TO, DIGIT = self.__convert_player_poker_coords_to_digit_prediction(config=config, coords=coords, roi=roi, MODEL_TYPE='player-pot')

            if BELONGS_TO in [1, 2, 3, 4, 5, 6, 7, 8]:
                self.__overall[BELONGS_TO]['pot'] = str(DIGIT)

        elif name == 'accepted_pot' and len(coords) > 0:
            roi = screenshot[CENTER_Y-15:CENTER_Y+15, CENTER_X-80:CENTER_X+80]
            DIGIT = self.__convert_board_bet_coords_to_digit_prediction(roi=roi, MODEL_TYPE='accepted_pot')
            self.__overall['board']['potential_bet'] = str(DIGIT) if str(DIGIT) != 0 else  '-'

        elif name == 'non_accepted_pot' and len(coords) > 0:
            roi = screenshot[CENTER_Y-15:CENTER_Y+15, CENTER_X-60:CENTER_X+60]
            DIGIT = self.__convert_board_bet_coords_to_digit_prediction(roi=roi, MODEL_TYPE='non_accepted_pot')
            self.__overall['board']['actual_bet'] = str(DIGIT) if str(DIGIT) != 0 else  '-'

        elif name == 'dealer':
            BELONGS_TO: str = self.__convert_coords_to_dealer_position(config=config, coords=coords)
            self.__overall['board']['dealer_position'] = str(BELONGS_TO)

        elif name == 'card' and len(coords) > 0:
            roi = screenshot[CENTER_Y-50:CENTER_Y+50, CENTER_X-40:CENTER_X+40]
            # One method for both board and player cards detection.
            BELONGS_TO, CARD, PRED_CHECK = self.__convert_coords_to_card_prediction(coords=coords, roi=roi)
            if PRED_CHECK:
                if BELONGS_TO != 0:
                    if BELONGS_TO == 'board':
                        # update board cards
                        self.__overall['board']['cards'].append(CARD)

                    if BELONGS_TO == 'player':
                        # update player cards
                        BELONGS_TO: str = self.__convert_coords_to_player_position(config=config, coords=coords)
                        self.__overall[int(BELONGS_TO)]['cards'].append(CARD)
                        self.__PLAYER_CARDS.append(CARD)
                        # check player in any position
                        if BELONGS_TO in ['1', '2', '3', '4', '5', '6', '7', '8']:
                            self.__overall['player']['position'] = BELONGS_TO

        elif name == 'opponent':
            BELONGS_TO: str = self.__convert_coords_to_player_position(config=config, coords=coords)
            if BELONGS_TO in ['1', '2', '3', '4', '5', '6', '7', '8']:
                self.__overall[int(BELONGS_TO)]['in_game'] = True

        elif name == 'action':
            self.__overall['player']['action'] = True

    def __update_player_data(self):
        bet_list = []
        for i in range(1, 7):
            if self.__overall[i]['bet'] == '-':
                bet_list.append(0)
            else:
                bet_list.append(float(self.__overall[i]['bet']))
        MAX_BET = max(bet_list)

        PLAYER_POSITION: int = self.__overall['player']['position']
        if PLAYER_POSITION != '-':
            player_data: dict = self.__overall[int(PLAYER_POSITION)]
            PLAYER_BET = 0 if player_data['bet'] == '-' else float(self.__overall[int(PLAYER_POSITION)]['bet'])

            self.__overall['player']['call'] = MAX_BET - PLAYER_BET
            self.__overall['player']['pot'] = player_data['pot']
            self.__overall['player']['bet'] = str(PLAYER_BET)
            self.__overall['player']['cards'] = player_data['cards']
            self.__overall[int(PLAYER_POSITION)]['in_game'] = True

    def run(self, predictor, config):
        data = screen_capture.updated_screenshot
        if len(data) == 0:
            return

        preds = predictor.run(MODEL_TYPE='board', image=data)

        names = preds[0].names
        boxes = preds[0].boxes

        self.__update(PLAYER_QUANTITY=config['board']['players'])
        for IDX, (cls, coords) in enumerate(zip(boxes.cls.tolist(), boxes.xyxy)):
            self.__parse(IDX=IDX, name=names[int(cls)], coords=coords, screenshot=data, config=config)

        self.__overall['board']['cards'] = sort_cards(self.__overall['board']['cards'])
        for i in range(1, 7):
            if len(self.__overall[i]['cards']) > 0:
                self.__overall[i]['cards'] = sort_cards(self.__overall[i]['cards'])
        self.__overall['board']['cards'] = sort_cards(self.__overall['board']['cards'])

        if self.client.get(name='game-data') is None:
            PREV_ACTION = False
        else:
            PREV_ACTION: bool = json.loads(self.client.get(name='game-data'))['player']['action']
        CURRENT_ACTION: bool = self.__overall['player']['action']

        self.__overall['action_started'] = True if not PREV_ACTION and CURRENT_ACTION else False
        self.__overall['action_ended'] = False if not PREV_ACTION and CURRENT_ACTION else True

        if self.client.get('game-data')['new_hand']:
            table_data['new_hand'] = False
            JSON_DATA = json.dumps(table_data)
            self.client.set('game-data', JSON_DATA)
            self.__overall['current_prompt_id'] = random.choice(range(1, 11))
            print(self.__overall['current_prompt_id'])

        self.__update_player_data()

    @property
    def table_data(self):
        return self.__overall
