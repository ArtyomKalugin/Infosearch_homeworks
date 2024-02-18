from crawler import Crawler


if __name__ == '__main__':
    crawler = Crawler(["https://theukdomain.uk/"], 2)
    crawler.crawl()