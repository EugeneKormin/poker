import cv2
from ultralytics import YOLO
import torch


class Predictor(object):
    _instance = None

    def __new__(cls, config):
        if cls._instance is None:
            cls._instance = super(Predictor, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, config):
        if self.__initialized:
            return
        print('models are initialized')
        self.__config = config

        self.__models = {
            'board': YOLO(self.__config['models']['board_detector']['path']).to('cuda'),
            'player-pot': YOLO(self.__config['models']['player-pot_detector']['path']).to('cuda'),
            'accepted_pot': YOLO(self.__config['models']['accepted_pot_detector']['path']).to('cuda'),
            'non_accepted_pot': YOLO(self.__config['models']['non_accepted_pot_detector']['path']).to('cuda'),
            'bet_detector': YOLO(self.__config['models']['bet_detector']['path']).to('cuda'),
            'card_detector': YOLO(self.__config['models']['card_detector']['path']).to('cuda')
        }
        self.__initialized = True

    def run(self, image, MODEL_TYPE: str = 'card_detector'):
        yolo_model = self.__models[MODEL_TYPE]
        return yolo_model.predict(image, verbose=False)
