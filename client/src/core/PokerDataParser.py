from src.core.PokerTableDistributor import PokerTableDistributor
from src.core.Predictor import Predictor
from src.utils.DataProcessor import extract_digits_from_predictions, extract_card_from_predictions, sort_cards
from src.utils.ScreenCapture import ScreenCapture

screen_capture = ScreenCapture()
poker_table_distributor = PokerTableDistributor()


class PokerDataParser(object):
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
                'board': {'cards': [], 'potential_bet': '0', 'actual_bet': '0', 'dealer_position': '0', 'my_position': '-'},
                'action': False,
                'counter': {'hand': 0, 'action': 0},
            }

        if PLAYER_QUANTITY == 8:
            self.__overall = {
                'out_of_table': {},
                1: {'pot': '-', 'bet': '-', 'cards': [], 'in_game': False},
                2: {'pot': '-', 'bet': '-', 'cards': [], 'in_game': False},
                3: {'pot': '-', 'bet': '-', 'cards': [], 'in_game': False},
                4: {'pot': '-', 'bet': '-', 'cards': [], 'in_game': False},
                5: {'pot': '-', 'bet': '-', 'cards': [], 'in_game': False},
                6: {'pot': '-', 'bet': '-', 'cards': [], 'in_game': False},
                7: {'pot': '-', 'bet': '-', 'cards': [], 'in_game': False},
                8: {'pot': '-', 'bet': '-', 'cards': [], 'in_game': False},
                'board': {'cards': [], 'potential_bet': '0', 'actual_bet': '0', 'dealer_position': '0',
                          'my_position': '-'},
                'action': False,
                'counter': {'hand': 0, 'action': 0},
            }

    def __convert_bet_coords_to_digit_prediction(self, config,  coords, roi, MODEL_TYPE: str):
        BELONGS_TO = poker_table_distributor.distribute_bets(config=config, coords=coords)

        try:
            preds = self.__predict.run(MODEL_TYPE=MODEL_TYPE, image=roi)
            DIGIT = extract_digits_from_predictions(preds=preds)
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
        
        CARD = extract_card_from_predictions(preds=preds)
        return BELONGS_TO, CARD

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
            BELONGS_TO, CARD = self.__convert_coords_to_card_prediction(coords=coords, roi=roi)
            if BELONGS_TO != 0:
                if BELONGS_TO == 'board':
                    # update board cards
                    self.__overall['board']['cards'].append(CARD)
                if BELONGS_TO == 'player':
                    # update player cards
                    BELONGS_TO: str = self.__convert_coords_to_player_position(config=config, coords=coords)
                    self.__overall[int(BELONGS_TO)]['cards'].append(CARD)
                    # check player in any position
                    if BELONGS_TO in ['1', '2', '3', '4', '5', '6', '7', '8']:
                        self.__overall['board']['my_position'] = BELONGS_TO

        elif name == 'opponent':
            BELONGS_TO: str = self.__convert_coords_to_player_position(config=config, coords=coords)
            if BELONGS_TO in ['1', '2', '3', '4', '5', '6', '7', '8']:
                self.__overall[int(BELONGS_TO)]['in_game'] = True

        elif name == 'action':
            self.__overall['action'] = True


    def run(self, predictor, config):
        updated_screenshot = screen_capture.updated_screenshot

        preds = predictor.run(MODEL_TYPE='board', image=updated_screenshot)

        names = preds[0].names
        boxes = preds[0].boxes

        self.__update(PLAYER_QUANTITY=config['board']['players'])
        for IDX, (cls, coords) in enumerate(zip(boxes.cls.tolist(), boxes.xyxy)):
            self.__parse(IDX=IDX, name=names[int(cls)], coords=coords, screenshot=updated_screenshot, config=config)

        self.__overall['board']['cards'] = sort_cards(self.__overall['board']['cards'])
        for i in range(1, 7):
            if len(self.__overall[i]['cards']) > 0:
                self.__overall[i]['cards'] = sort_cards(self.__overall[i]['cards'])
        self.__overall['board']['cards'] = sort_cards(self.__overall['board']['cards'])

    @property
    def table_data(self):
        return self.__overall
