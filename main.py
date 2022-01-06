import re
from typing import Counter, List, Tuple
from itertools import count

class Guesser:

    def __init__(self) -> None:
        self.valid = [] # type: List[str]
        with open('5_letter_words.wl', encoding='UTF-8') as file:
            while line := file.readline():
                line = line.replace('\n', '').strip()
                self.valid.append(line)

    def add(self, guess: str, mask: Tuple[int, int, int, int, int]) -> None:
        guess_c = Counter(guess)
        for char in guess_c:
            temp = zip(guess, mask, count(0))
            char_list = [(m, i) for c, m, i in temp if c == char]
            exact = []
            loc = []
            at_least = True
            for m, i in char_list:
                if m == 1:
                    loc.append(i)
                elif m == 2:
                    exact.append(i)
                elif m == 0:
                    at_least = False
            if not exact and not loc:
                self.filter_none(char)
            if exact:
                self.filter_exact(char, exact)
            if loc:
                self.filter_loc(char, loc, exact, at_least)

    def filter_none(self, char: str) -> None:
        pat = re.compile('^[^' + char + ']*$')
        self.valid = [word for word in self.valid if pat.match(word)]

    def filter_exact(self, char: str, indexes: List[int]) -> None:
        for index in indexes:
            if index > 0:
                start = '^.{' + str(index) + '}'
            else:
                start = '^'
            if index < 4:
                end = '.{' + str(4 - index) + '}$'
            else:
                end = '$'
            pat = re.compile(start + char + end)
            self.valid = [word for word in self.valid if pat.match(word)]

    def filter_loc(
        self,
        char: str,
        indexes: List[int],
        exact_indexes: List[int],
        at_least: bool) -> None:
        num = len(indexes) + len(exact_indexes)
        pat_str = '^([^' + char + ']*' + char + '){' + str(num)
        if at_least:
            pat_str += ','
        pat_str += '}[^' + char + ']*$'
        pat = re.compile(pat_str)
        self.valid = [word for word in self.valid if pat.match(word)]
        self.filter_exact('[^' + char + ']', indexes)

    def print(self) -> None:
        num = len(self.valid)
        print(num)
        for i in range(min(num, 50)):
            print(self.valid[i])

G = Guesser()
G.add('eagle', (1,0,2,0,0))
G.add('begin', (0,1,2,1,0))
G.print()
