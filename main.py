from hw1.crawler import Crawler
from hw2.lemmaHelper import LemmaHelper
import os
from fileHelper import FileHelper


if __name__ == '__main__':
    # HW1
    # crawler = Crawler(["https://theukdomain.uk/"], 2)
    # crawler.crawl()

    # HW 2
    result_text = []
    file_helper = FileHelper()

    for file in os.listdir("results"):
        file_path = os.path.join('results', file)
        result_text.append(file_helper.get_html_text(file_path))

    lemma_helper = LemmaHelper()
    lemma_helper.make_lemmas(" ".join(result_text))