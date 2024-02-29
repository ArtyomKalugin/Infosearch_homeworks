import os
from collections import defaultdict
from fileHelper import FileHelper
from hw2.lemmaHelper import LemmaHelper

class IndexInverter:
    def __init__(self):
        self.inverted_indexes = defaultdict(list)

    def make_inverted_index(self):
        file_helper = FileHelper()
        lemma_helper = LemmaHelper()
        index = 1

        for file in os.listdir("results"):
            result_text = []
            file_path = os.path.join('results', file)
            result_text.append(file_helper.get_html_text(file_path))

            lemma_helper = LemmaHelper()
            lemma_helper.make_lemmas(" ".join(result_text))

            for lemma in lemma_helper.lemmas.keys():
                self.inverted_indexes[lemma].append(index)

            index += 1