import re
from typing import Counter, List, Tuple
from itertools import count
from functools import cmp_to_key

class Guesser:

    def __init__(self) -> None:
        self.valid = [] # type: List[str]
        self.freqs = Counter('abccd')
        self.known = [] # type: List[str]
        with open('5_letter_words.wl', encoding='UTF-8') as file:
            while line := file.readline():
                line = line.replace('\n', '').strip()
                self.valid.append(line)

    def add(self, guess: str, mask: Tuple[int, int, int, int, int]) -> None:
        self.known = [] # type: List[str]
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
                    self.known.append(char)
                elif m == 2:
                    exact.append(i)
                    self.known.append(char)
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
            start = '^' if index == 0 else '^.{' + str(index) + '}'
            end = '$' if index == 4 else '.{' + str(4 - index) + '}$'
            pat_str = start + char + end
            pat = re.compile(pat_str)
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

    def sort_valid(self) -> None:
        self.freqs = Counter(''.join(self.valid))
        self.valid = sorted(self.valid, key=cmp_to_key(self.compare))

    def compare(self, item1: str, item2: str) -> int:
        return self.word_value(item2) - self.word_value(item1)

    def word_value(self, word: str) -> int:
        output = 0
        seen = []
        for char in word:
            if char in seen and char not in self.known:
                continue
            seen.append(char)
            output += self.freqs[char]
            if char in self.known:
                output -= len([x for x in self.known if x == char]) * len(self.valid)
        return output

    def print(self) -> None:
        self.sort_valid()
        num = len(self.valid)
        print(num)
        for i in range(min(num, 50)):
            print(self.valid[i])

G = Guesser()
G.add('arose', (1,2,0,0,0))
G.add('train', (0,2,2,0,1))
G.add('drank', (0,2,2,2,2))
#G.add('canal', (0,2,2,2,2))
G.print()
