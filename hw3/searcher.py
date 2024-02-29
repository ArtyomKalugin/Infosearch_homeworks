import json
from collections import defaultdict
import pymorphy2


class Searcher:
    AND = "&"
    OR = "|"
    NOT = "~"
    OPERATORS = (AND, OR, NOT)

    def __init__(self):
        self.inverted_indexes = self.get_inverted_indexes()
        self.morphy = pymorphy2.MorphAnalyzer()

    def search(self, request):
        words = request.strip().split()
        all_indexes = set.union(*self.inverted_indexes.values())
        result = set()
        i = 0

        while i < len(words):
            word = words[i]
            if i + 1 != len(words) and (word in (self.AND or self.OR)):
                next_word = words[i + 1]
                if word == self.AND:
                    result = result.intersection(
                        self.inverted_indexes[self.get_normal_form(next_word)]
                    )
                elif word == self.OR:
                    result = result.union(
                        self.inverted_indexes[self.get_normal_form(next_word)]
                    )
                i += 1
            elif word.startswith(self.NOT):
                result = result.union(
                    all_indexes.difference(
                        self.inverted_indexes[self.get_normal_form(word[1:])]
                    )
                )
            else:
                result = result.union(self.inverted_indexes[self.get_normal_form(word)])
            i += 1

        return result

    def get_inverted_indexes(self):
        inverted_indexes = defaultdict(set)
        with open("inverted_indexes/inverted_indexes.txt") as f:
            for line in f.readlines():
                index = json.loads(line.replace("'", '"').strip())
                inverted_indexes[index["word"]] = set(index["inverted"])

        return inverted_indexes

    def get_normal_form(self, word):
        morph = self.morphy.parse(word)

        return morph[0].normal_form
