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
        self.result_list = []
        self.parsed_links = []


    def parse_html(self, url):
        """Method for parsing html of input url
        :Parameters:

        :Return:
            None
        """
        page = requests.get(url)
        tree = html.fromstring(page.content)
        self.parsed_links.extend([link for link in tree.xpath('//a/@href')\
                                 if '://www.' in link or 'mailto:' in link])


    def extract_url(self, url):
        """Method for getting domain and ip
        from parsed url
        :Parameters:
            -url - url from parsed html
        :Return:
            None
        """
        domain = urlparse(url).netloc[4:]
        ip = socket.gethostbyname(domain)
        self.result_list.append([url, domain, ip])


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
        for res in self.result_list:
            print '{} - {} - {}'.format(*res)


    def run(self):
        """Main class method
        :Parameters:
        :Return:
            return result list
        """
        for url in self.input_urls:
            self.parse_html(url)
            for link in self.parsed_links:
                self.extract_url(link)
        return self.result_list


if __name__ == '__main__':
    crawler = Crawler(sys.argv[1:])
    crawler.run()
    crawler.print_result()
