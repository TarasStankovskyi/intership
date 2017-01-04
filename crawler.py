import argparse
import socket
from lxml import html
from urlparse import urlparse
import requests




PARSER = argparse.ArgumentParser()
PARSER.add_argument('web_pages', nargs='+',
                    help='list of web pages for crawler')
ARGS = PARSER.parse_args()

class Crawler(object):

    def __init__(self, args):
        self.output = {}
        for x in args:
            self.output[x] = {}


    def parse_HTML(self):
        self.links = []
        for source in self.output:
            page = requests.get(source)
            tree = html.fromstring(page.content)
            self.links.extend([link for link in tree.xpath('//a/@href') if '://www.' in link\
                              or 'mailto:' in link])
            for link in self.links:
               self.output[source][link] = []


    def set_domain(self):
        for source in self.output:
            for url in self.output[source]:
               self.output[source][url].append(urlparse(url).netloc[4:])



    def set_IP(self):
        for source in self.output:
            for url in self.output[source]:
                self.output[source][url].append(socket.gethostbyname(self.output[source][url][0]))


    def print_out(self):
        result = []
        for url in self.output.values():
            result.extend(url.items())
        for url in result:
            print '{} - {}\n'.format(url[0], ' '.join(url[1]))

if __name__ == '__main__':
    crawler = Crawler(ARGS.web_pages)
    crawler.parse_HTML()
    crawler.set_domain()
    crawler.set_IP()
    crawler.print_out()
