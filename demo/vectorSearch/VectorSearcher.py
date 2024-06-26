import ast
import os
from pathlib import Path

import pymorphy2
from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer

BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_FILE_PATH = BASE_DIR.parent.joinpath("index.txt")
TF_IDF_FILES_DIR = BASE_DIR.parent.joinpath("lemmas_tf_idf")
INVERTED_INDEX_FILE_PATH = BASE_DIR.parent.joinpath("inverted_indexes").joinpath("inverted_indexes.txt")


class VectorSearcher:
    def __init__(self) -> None:
        self.tokenizer = WordPunctTokenizer()
        self.morph_analyzer = pymorphy2.MorphAnalyzer()
        self.pages = self.get_pages()
        self.lemmas = self.get_all_lemmas()
        self.tf_idf_matrix = self.get_tf_idf_matrix()

    def get_lemmas(self, query):
        lemmas = list()
        possible_tokens = self.tokenizer.tokenize(query)
        result_tokens = set()
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

            result_tokens.add(token)

        for token in result_tokens:
            morph = self.morph_analyzer.parse(token)
            if any([x for x in bad_tags if x in morph[0].tag]) or token in bad_words:
                continue

            if morph[0].score >= 0.4:
                lemmas.append(morph[0].normal_form)

        return lemmas

    def get_pages(self):
        pages = {}
        index = 0
        with open(INDEX_FILE_PATH) as f:
            for line in f.readlines():
                if index == 0 or index == 222:
                    index += 1
                    continue

                parts = line.split(maxsplit=2)
                key = parts[0].replace(':', '').replace("\"", '') + ".html"
                value = parts[1].replace("\"", '')
                pages[key] = value
                index += 1

        return pages

    def get_all_lemmas(self):
        lemmas = set()
        with open(INVERTED_INDEX_FILE_PATH) as f:
            for line in f.readlines():
                lemmas.add(ast.literal_eval(line)["word"])

        return list(lemmas)

    def get_tf_idf_matrix(self):
        matrix = dict()
        for root, _, files in os.walk(TF_IDF_FILES_DIR):
            for file in files:
                with open(os.path.join(root, file)) as f:
                    matrix[file] = {lemma: 0.0 for lemma in self.lemmas}
                    for line in f.readlines():
                        lemma, _, tf_idf = line.split(maxsplit=2)
                        matrix[file][lemma] = float(tf_idf)

        return matrix

    def get_query_vector(self, lemmas):
        vector = {lemma: 0 for lemma in self.lemmas}
        for lemma in lemmas:
            vector[lemma] = 1

        return vector

    def normalize_vector(self, vector):
        return sum([c**2 for c in vector]) ** 0.5

    def calculate_cosine_similarity(self, query_vector, page_vector):
        dot = sum(q * p for q, p in zip(query_vector, page_vector))
        if dot:
            return dot / (
                self.normalize_vector(query_vector) * self.normalize_vector(page_vector)
            )

        return 0

    def get_similarities(self, query_vector):
        similarities = {}
        for page, lemma_tf_idf in self.tf_idf_matrix.items():
            page_vector = list(lemma_tf_idf.values())
            similarity = self.calculate_cosine_similarity(query_vector, page_vector)
            if similarity:
                similarities[page.replace('.txt', '.html')] = similarity

        return sorted(
            [(self.pages[x[0]], x[1]) for x in similarities.items() if x[1] > 0.0],
            key=lambda x: x[1],
            reverse=True,
        )

    def search(self, query):
        query_lemmas = self.get_lemmas(query)
        query_vector = self.get_query_vector(query_lemmas)

        return self.get_similarities(list(query_vector.values()))

vector_searcher = VectorSearcher()