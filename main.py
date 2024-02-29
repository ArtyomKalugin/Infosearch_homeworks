from hw1.crawler import Crawler
from hw2.lemmaHelper import LemmaHelper
import os
from fileHelper import FileHelper
from hw3.indexInverter import IndexInverter
from hw3.searcher import Searcher

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
    index_inverter = IndexInverter()
    index_inverter.make_inverted_index()
    result = ""

    for word, inverted in index_inverter.inverted_indexes.items():
        result += str(
            {
                "word": word,
                "inverted": inverted,
                "count": len(inverted)
            }
        ) + "\n"

    file_helper.make_file(result, "inverted_indexes.txt", "inverted_indexes")

    # Search
    searcher = Searcher()
    search_strings = [
        "Skip browser",
        "Skip | browser",
        "Skip & browser",
        "~Skip & browser",
        "Skip & ~browser",
        "Skip | ~browser",
        "(Skip | ~browser) & Apple & Privacy"
    ]

    for string in search_strings:
        result = searcher.search(string)

        if len(result) == 0:
            print("NO RESULT!")
        else:
            print(result)
