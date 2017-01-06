import sys
import socket
from urlparse import urlparse
from lxml import html
import requests


class Crawler(object):
    """Class for getting iformation about
    all url's domain and ip that are in web page """


    def __init__(self, urls):
        """Crawler's init method
        :Parameters:
            -urls - input urls from console
        :Return:
            None
        """
        self.input_urls = urls
        self.result = {}
        self._parsed_links = {}


    def __parse_html(self, url):
        """Method for parsing html of input url
        :Parameters:

        :Return:
            None
        """

        page = requests.get(url)
        tree = html.fromstring(page.content)
        self._parsed_links[url] = ([link for link in tree.xpath('//a/@href')\
                                 if '://www.' in link or 'mailto:' in link])



    def __extract_url(self, url):
        """Method for getting domain and ip
        from parsed url
        :Parameters:
            -url - url from parsed html
        :Return:
            None
        """
        domain = urlparse(url).netloc[4:]
        ip = socket.gethostbyname(domain)
        return [url, domain, ip]


    def print_result(self):
        """Method for printing result
        :Parameters:
            -url - url from page's urls
            -domain - url's domain
            -ip - url's ip
        :Return:
            string "URL - domain - ip"
            example "http://www.bbc.co.uk/news/ - bbc.co.uk - 212.58.246.78"
        """
        for result in self.result.values():
            for res in result:
                print '{} - {} - {}'.format(*res)


    def run(self):
        """Main class method
        :Parameters:
        :Return:
            return result list
        """
        for url in self.input_urls:
            self.__parse_html(url)
        for link in self._parsed_links:
            self.result[link] = []
            for url in self._parsed_links[link]:
                self.result[link].append(self.__extract_url(url))
        self.print_result()
        return self.result


if __name__ == '__main__':
    crawler = Crawler(sys.argv[1:])
    crawler.run()
