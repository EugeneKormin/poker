import json
import redis
from src.utils.DataProcessor import convert_string_to_hash


class DataTransmission:
    def __init__(self, SERVER_URL: str):
        self.redis_host = SERVER_URL
        self.redis_port = 6379
        self.client = redis.StrictRedis(host=self.redis_host, port=self.redis_port, decode_responses=True)
        self.__first_game = True

    def send_poker_data(self, table_data: dict):
        DATA_IS_READY_TO_BE_SENT: bool = self.__check_data_for_consistency(json_data=table_data)

        # and table_data['action']
        if DATA_IS_READY_TO_BE_SENT:
            previous_data: str = self.client.get('game-data')
            if previous_data is None:
                previous_data = ''
            current_data: str = json.dumps(table_data)

            NEW_HASH = convert_string_to_hash(STR=previous_data)
            CURRENT_HASH = convert_string_to_hash(STR=current_data)

            if NEW_HASH != CURRENT_HASH:

                if previous_data == '':
                    PREV_DEALER_POSITION = 0
                else:
                    PREV_DEALER_POSITION = json.loads(previous_data)['board']['dealer_position']
                CURRENT_DEALER_POSITION = json.loads(current_data)['board']['dealer_position']

                HAND, ACTION = self.__get_counter()
                if CURRENT_DEALER_POSITION != PREV_DEALER_POSITION or self.__first_game:
                    HAND += 1
                    ACTION = 0
                    self.__first_game = False
                else:
                    HAND = HAND
                    ACTION += 1

                updated_counter = {'hand': HAND, 'action': ACTION}
                table_data['counter']['hand'], table_data['counter']['action'] = HAND, ACTION

                json_data = json.dumps(table_data)

                self.client.set('hash', NEW_HASH)
                self.client.set("game-data", json_data)
                self.client.set('counter', json.dumps(updated_counter))
                self.client.publish('my_channel', json_data)

    @staticmethod
    def __check_data_for_consistency(json_data):
        for K, v in json_data.items():
            if K in [1, 2, 3, 4, 5, 6, 7, 8]:
                if (v['in_game'] and v['pot'] != '-') or not v['in_game']:
                    pass
                else:
                    return False
        return True

    def __get_counter(self):
        counter = self.client.get('counter')
        if counter is None:
            self.client.set('counter', json.dumps({'hand': 0, 'action': 0}))
        counter = json.loads(self.client.get('counter'))

        return counter['hand'], counter['action']

