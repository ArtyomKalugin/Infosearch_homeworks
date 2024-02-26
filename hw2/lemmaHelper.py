from collections import defaultdict

import nltk
import pymorphy2
from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer
from fileHelper import FileHelper


nltk.download("stopwords")


class LemmaHelper:
    def __init__(self):
        self.tokens = set()
        self.lemmas = defaultdict(set)

        self.tokenizer = WordPunctTokenizer()
        self.morph_analyzer = pymorphy2.MorphAnalyzer()

    def make_lemmas(self, text):
        possible_tokens = self.tokenizer.tokenize(text)

        bad_tokens = set()
        bad_tags = {"UNKN", "PREP", "CONJ", "PRCL", "INTJ", "PNCT", "NUMB", "ROMN"}
        bad_words = set(stopwords.words("english"))

        for token in possible_tokens:
            # Удаляем токены, которые содержат и буквы, и цифры
            contains_digits = False
            contains_letters = False

            for char in token:
                if char.isdigit():
                    contains_digits = True
                if char.isalpha():
                    contains_letters = True

            if (contains_letters and contains_digits) or (contains_digits and not contains_letters):
                continue

            self.tokens.add(token)

        for token in self.tokens:
            morph = self.morph_analyzer.parse(token)
            if any([x for x in bad_tags if x in morph[0].tag]) or token in bad_words:
                bad_tokens.add(token)
                continue

            if morph[0].score >= 0.5:
                self.lemmas[morph[0].normal_form].add(token)

        self.tokens = self.tokens - bad_tokens

        file_helper = FileHelper()
        file_helper.make_file("\n".join(self.tokens), "tokens.txt", "tokens")

        lemmas_to_write = ""
        for token, lemmas in self.lemmas.items():
            lemmas_to_write += f"{token}: {' '.join(lemmas)}\n"

        file_helper.make_file(lemmas_to_write, "lemmas.txt", "lemmas")
