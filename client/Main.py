from src.core.Predictor import Predictor
from src.core.PokerDataParser import PokerDataParser
from src.services.PokerDataTransmission import DataTransmission
from src.utils.LoadConfig import load_config
from src.services.SLM import SLM


def run():
    config = load_config(config_path='./config/config.yaml')

    predictor = Predictor(config=config)
    poker_data_parser = PokerDataParser(config=config)
    slm = SLM()

    transmission_service = DataTransmission(config=config)
    while True:
        poker_data_parser.run(predictor=predictor, config=config)
        table_data = poker_data_parser.table_data
        # table_data = slm.get_response(table_data=table_data)
        transmission_service.send_poker_data(table_data=table_data)


if __name__ == '__main__':
    run()
