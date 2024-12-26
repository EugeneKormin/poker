import json
import redis
from client.src.utils.DataProcessor import convert_string_to_hash


class DataTransmission:
    def __init__(self, config: dict):
        self.redis_host = config['server']['url']
        self.redis_port = config['server']['redis_port']
        self.client = redis.StrictRedis(host=self.redis_host, port=self.redis_port, decode_responses=True)
        self.__ACTION = -1
        self.__HASH = ''
        self.__CURRENT_POT = -1
        self.__INIT_POT_REMEMBERED = False
        self.__PROMPT_ID_REMEMBERED = False
        self.__PREV_DEALER_POSITION = -1
        self.__PREV_PLAYER_POT = 0
        self.__DIFF_WITH_PREV_HAND = 0
        self.__PREV_PROMPT_ID = -1
        self.__analytics: dict = {'prompt_id': self.__PREV_PROMPT_ID, 'diff': self.__DIFF_WITH_PREV_HAND}

    def __update_hand_id(self, table_data: dict) -> dict:
        CURRENT_DEALER_POSITION = table_data['board']['dealer_position']

        if CURRENT_DEALER_POSITION != self.__PREV_DEALER_POSITION:
            self.__ACTION = 0
            self.__INIT_POT_REMEMBERED = False
            self.__PROMPT_ID_REMEMBERED = False
            table_data['new_hand'] = True
            self.__HASH = convert_string_to_hash(STR=json.dumps(table_data))
            self.__PREV_DEALER_POSITION = CURRENT_DEALER_POSITION

        table_data['board']['hand_id'] = f'{self.__HASH[:4]}...{self.__HASH[-4:]}'
        return table_data

    def __update_action_phase(self, table_data: dict) -> dict:
        if table_data['action_started']:
            self.__ACTION += 1
            self.__POT = table_data['player']['pot']

        table_data['player']['action_counter'] = self.__ACTION
        return table_data

    def __update_init_player_pot(self, table_data: dict):
        if not self.__INIT_POT_REMEMBERED:
            BET = 0 if table_data['player']['bet'] == '-' else float(table_data['player']['bet'])
            if table_data['player']['pot'] != '-':
                CURRENT_POT = float(table_data['player']['pot']) + BET
                self.__DIFF_WITH_PREV_HAND = CURRENT_POT - self.__PREV_PLAYER_POT
                self.__PREV_PLAYER_POT = CURRENT_POT
                self.__INIT_POT_REMEMBERED = True

    def __prepare_analytics_data(self, table_data: dict) -> None:
        if not self.__PROMPT_ID_REMEMBERED and table_data['player']['position'] != '-':
            self.__analytics: dict = {'prompt_id': self.__PREV_PROMPT_ID, 'diff': self.__DIFF_WITH_PREV_HAND}
            self.__PREV_PROMPT_ID = table_data['current_prompt_id']
            self.__PROMPT_ID_REMEMBERED = True

    def __send_table_data(self, updated_data: dict):
        DATA_IS_READY_TO_BE_SENT: bool = self.__check_data_for_consistency(json_data=updated_data)
        if DATA_IS_READY_TO_BE_SENT:
            UPDATED_JSON_DATA: str = json.dumps(updated_data)
            self.client.set("game-data", UPDATED_JSON_DATA)
            self.client.publish('my_channel', UPDATED_JSON_DATA)

    def __send_analytics_data(self, analytics_data: dict):
        ANALYTICS_JSON_DATA: str = json.dumps(analytics_data)
        self.client.set("analytics", ANALYTICS_JSON_DATA)

    def send_poker_data(self, table_data: dict):
        updated_data: dict = self.__update_hand_id(table_data=table_data)
        updated_data: dict = self.__update_action_phase(table_data=updated_data)
        self.__update_init_player_pot(table_data=updated_data)
        # self.__prepare_analytics_data(table_data=updated_data)
        self.__send_table_data(updated_data=updated_data)
        '''
        if self.__ACTION == 0:
            self.__send_analytics_data(analytics_data=self.__analytics)
        '''

    @staticmethod
    def __check_data_for_consistency(json_data):
        for K, v in json_data.items():
            if K in [1, 2, 3, 4, 5, 6, 7, 8]:
                if v['in_game']:
                    if v['pot'] != '-':
                        pass
                    else:
                        return False
        return True
