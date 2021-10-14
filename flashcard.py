import alarm

from json import load
from random import random

class Flashcard:
    def __init__(self):
        with open("/deck.json") as file:
            self._deck = load(file)

    @property
    def _mode(self):
        return alarm.sleep_memory[0]

    @_mode.setter
    def _mode(self, value) -> None:
        alarm.sleep_memory[0] = value

    @property
    def _week(self):
        return alarm.sleep_memory[1]

    @_week.setter
    def _week(self, value) -> None:
        alarm.sleep_memory[1] = value

    @property
    def _word(self):
        return alarm.sleep_memory[2]

    @_word.setter
    def _word(self, value) -> None:
        alarm.sleep_memory[2] = value

    @property
    def _cards(self):
        return self._deck["cards"]

    @property
    def mode_text(self) -> str:
        return self._deck["modes"][self._mode]

    @property
    def week_text(self) -> str:
        return "Week {}".format(self._week + 1)

    @property
    def word_text(self) -> str:
        return self._cards[self._mode][self._week][self._word]

    def next_mode(self) -> None:
        self.refresh = True

        modes = len(self._cards)

        self._mode = (self._mode + 1) % modes
        self._word = 0

        print("self._mode: {}".format(self._mode))
        print("self._week: {}".format(self._week))
        print("self._word: {}".format(self._word))

    def next_week(self) -> None:
        self.refresh = True

        weeks = len(self._cards[self._mode])

        self._week = (self._week + 1) % weeks
        self._word = 0

        print("self._mode: {}".format(self._mode))
        print("self._week: {}".format(self._week))
        print("self._word: {}".format(self._word))

    def next_word(self) -> None:
        self.refresh = True

        words = len(self._cards[self._mode][self._week])

        self._word = (self._word + 1) % words

        print("self._mode: {}".format(self._mode))
        print("self._week: {}".format(self._week))
        print("self._word: {}".format(self._word))

    def shuffle_words(self) -> None:
        self.refresh = True

        words = self._cards[self._mode][self._week]

        words = sorted(words, key=lambda _: random())

        self._cards[self._mode][self._week] = words
        self.card = 0

        print("self._mode: {}".format(self._mode))
        print("self._week: {}".format(self._week))
        print("self._word: {}".format(self._word))
