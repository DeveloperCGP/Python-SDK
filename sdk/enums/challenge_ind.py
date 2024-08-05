from enum import Enum


class ChallengeInd(Enum):
    CI_01 = "01"
    CI_02 = "02"
    CI_03 = "03"
    CI_04 = "04"
    CI_05 = "05"
    CI_06 = "06"
    CI_07 = "07"
    CI_08 = "08"
    CI_09 = "09"

    def __init__(self, value):
        self._value_ = value

    def get_value(self):
        return self.value

    @staticmethod
    def get_challenge_ind(string_value: str):
        for challengeInd in ChallengeInd:
            if string_value == challengeInd.value:
                return challengeInd
        return None
