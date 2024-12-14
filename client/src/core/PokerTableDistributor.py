

class PokerTableDistributor:
    @staticmethod
    def __coords2coeffs(coords):
        return round(((int(coords[0]) + int(coords[2])) // 2) / 1024, 2), round(((int(coords[1]) + int(coords[3])) // 2) / 768, 2)


    def distribute_bets(self, config, coords) -> int:
        coeff1, coeff2 = self.__coords2coeffs(coords=coords)

        PLAYER_QUANTITY: int = config['board']['players']

        if PLAYER_QUANTITY == 8:
            if 0 < coeff1 < 0.4:
                if 0 < coeff2 < 0.45:
                    return 1
                elif 0.45 < coeff2 < 0.55:
                    return 8
                elif 0.55 < coeff2:
                    return 7
            elif 0.4 < coeff1 < 0.6:
                if coeff2 < 0.5:
                    return 2
                else:
                    return 6
            elif 0.6 < coeff1 < 0.85:
                if 0 < coeff2 < 0.45:
                    return 3
                elif 0.45 < coeff2 < 0.55:
                    return 4
                elif 0.55 < coeff2:
                    return 5
            elif 0.85 < coeff1:
                return 4

        if PLAYER_QUANTITY == 6:
            if 0.66 > coeff1 > 0.33:
                return 5 if coeff2 > 0.5 else 2
            elif 0.33 > coeff1:
                return 6 if coeff2 > 0.5 else 1
            elif coeff1 > 0.66:
                return 4 if coeff2 > 0.5 else 3
            else:
                return 0

    def distribute_player_pots(self, config, coords):
        coeff1, coeff2 = self.__coords2coeffs(coords=coords)

        PLAYER_QUANTITY: int = config['board']['players']

        if PLAYER_QUANTITY == 8:
            if 0 < coeff1 < 0.15:
                return 8
            elif 0.15 < coeff1 < 0.4:
                if coeff2 < 0.5:
                    return 1
                else:
                    return 7
            elif 0.4 < coeff1 < 0.6:
                if coeff2 < 0.5:
                    return 2
                else:
                    return 6
            elif 0.6 < coeff1 < 0.85:
                if coeff2 < 0.5:
                    return 3
                else:
                    return 5
            elif 0.85 < coeff1:
                return 4

        if PLAYER_QUANTITY == 6:
            if 0.66 > coeff1 > 0.33:
                return 5 if coeff2 > 0.5 else 2
            elif 0.33 > coeff1:
                return 6 if coeff2 > 0.5 else 1
            elif coeff1 > 0.66:
                return 4 if coeff2 > 0.5 else 3
            else:
                return 0


    def distribute_cards(self, coords) -> str:
        coeff1, coeff2 = self.__coords2coeffs(coords=coords)

        return 'board' if 0.3 < coeff1 < 0.7 and 0.45 < coeff2 < 0.55 else 'player'


    def distributed_cards2player_position(self, config, coords) -> int:
        coeff1, coeff2 = self.__coords2coeffs(coords=coords)

        PLAYER_QUANTITY: int = config['board']['players']

        if PLAYER_QUANTITY == 6:
            if 0.66 > coeff1 > 0.33:
                return 5 if coeff2 > 0.5 else 2
            elif 0.33 > coeff1:
                return 6 if coeff2 > 0.5 else 1
            elif coeff1 > 0.66:
                return 4 if coeff2 > 0.5 else 3
            else:
                return 0
        elif PLAYER_QUANTITY == 8:
            if 0 < coeff1 < 0.15:
                return 8
            elif 0.15 < coeff1 < 0.4:
                if coeff2 < 0.5:
                    return 1
                else:
                    return 7
            elif 0.4 < coeff1 < 0.6:
                if coeff2 < 0.5:
                    return 2
                else:
                    return 6
            elif 0.6 < coeff1 < 0.85:
                if coeff2 < 0.5:
                    return 3
                else:
                    return 5
            elif 0.85 < coeff1:
                return 4


    def distributed_cards2dealer_position(self, config, coords):
        PLAYER_QUANTITY: int = config['board']['players']

        coeff1, coeff2 = self.__coords2coeffs(coords=coords)

        if PLAYER_QUANTITY == 6:
            if 0.66 > coeff1 > 0.33:
                return 5 if coeff2 > 0.5 else 2
            elif 0.33 > coeff1:
                return 6 if coeff2 > 0.5 else 1
            elif coeff1 > 0.66:
                return 4 if coeff2 > 0.5 else 3
            else:
                return 0
        elif PLAYER_QUANTITY == 8:
            if coeff2 < 0.32:
                if coeff1 < 0.35:
                    return 1
                elif 0.35 < coeff1 < 0.55:
                    return 2
                elif coeff1 > 0.55:
                    return 3
            elif 0.32 < coeff2 < 0.5:
                if coeff1 < 0.5:
                    return 8
                elif coeff1 > 0.5:
                    return 4
            elif coeff2 > 0.5:
                if coeff1 < 0.31:
                    return 7
                elif 0.31 < coeff1 < 0.69:
                    return 6
                elif coeff1 > 0.69:
                    return 5

