from hw1.crawler import Crawler
from hw2.lemmaHelper import LemmaHelper
import os
import math
from fileHelper import FileHelper
from hw3.indexInverter import IndexInverter
from hw3.searcher import Searcher
from hw4.tfidHelper import TFIDHelper
from collections import Counter
from hw5.VectorSearcher import VectorSearcher


def idf_word_counter(files_texts, word):
    count = 0
    for file_name, text in files_texts.items():
        if word in text:
            count += 1
    if count > 100:
        print(word, count)
    return count


if __name__ == '__main__':
    file_helper = FileHelper()

    # HW1 -----------------------------------------------------------------------
    # crawler = Crawler(["https://theukdomain.uk/"], 2)
    # crawler.crawl()

    # HW2 -----------------------------------------------------------------------
    # result_text = []
    #
    # for file in os.listdir("results"):
    #     file_path = os.path.join('results', file)
    #     result_text.append(file_helper.get_html_text(file_path))
    #
    # lemma_helper = LemmaHelper()
    # lemma_helper.make_lemmas(" ".join(result_text))

    # HW3 -----------------------------------------------------------------------
    # index_inverter = IndexInverter()
    # index_inverter.make_inverted_index()
    # result = ""
    #
    # for word, inverted in index_inverter.inverted_indexes.items():
    #     result += str(
    #         {
    #             "word": word,
    #             "inverted": inverted,
    #             "count": len(inverted)
    #         }
    #     ) + "\n"
    #
    # file_helper.make_file(result, "inverted_indexes.txt", "inverted_indexes")
    #
    # # Search
    # searcher = Searcher()
    # search_strings = [
    #     "Skip browser",
    #     "Skip | browser",
    #     "Skip & browser",
    #     "~Skip & browser",
    #     "Skip & ~browser",
    #     "Skip | ~browser",
    #     "(Skip | ~browser) & Apple & Privacy"
    # ]
    #
    # for string in search_strings:
    #     result = searcher.search(string)
    #
    #     if len(result) == 0:
    #         print("NO RESULT!")
    #     else:
    #         print(result)

    # HW4 -----------------------------------------------------------------------
    # files_texts = {}
    # for root, _, files in os.walk("results"):
    #     for index, file in enumerate(sorted(files), 1):
    #         text = file_helper.get_html_text(os.path.join(root, file))
    #         files_texts[file] = text
    #
    # full_text = " ".join(files_texts.values())
    # full_text_calc = TFIDHelper(full_text)
    # for file_name, text in files_texts.items():
    #     text_cals = TFIDHelper(text)
    #     words_counter = Counter(text_cals.tokenizer_result)
    #     new_filename = f"{file_name.split('.')[0]}.txt"
    #     tokens_result = ""
    #
    #     for token in text_cals.tokens:
    #         tf = words_counter[token] / len(text_cals.tokenizer_result)
    #         idf = math.log(len(files_texts) / idf_word_counter(files_texts, token))
    #         tf_idf = tf * idf
    #         tokens_result += f"{token} {idf} {tf_idf}\n"
    #
    #     file_helper.make_file(tokens_result, new_filename, "tokens_tf_idf")
    #
    #     lemmas_result = ""
    #     for lemma, tokens in text_cals.lemmas.items():
    #         tf_n = words_counter[lemma]
    #         for token in tokens:
    #             tf_n += words_counter[token]
    #         count = 0
    #         for text in files_texts.values():
    #             if any(token in text for token in tokens) or lemma in text:
    #                 count += 1
    #
    #         tf = tf_n / len(text_cals.tokenizer_result)
    #         idf = math.log(len(files_texts) / count)
    #         tf_idf = tf * idf
    #         lemmas_result += f"{lemma} {idf} {tf_idf}\n"
    #
    #     file_helper.make_file(lemmas_result, new_filename, "lemmas_tf_idf")

    # HW5 -----------------------------------------------------------------------
    vector_searcher = VectorSearcher()
    print(vector_searcher.search("Welcome to Nominet’s privacy notice."))