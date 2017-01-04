import sys
import socket
from urlparse import urlparse
from lxml import html
import requests


class Crawler(object):
    """Class for getting iformation about all url's domain and ip that are in web page """


    def __init__(self, url):
        """Crawler's init method
        :Parameters:
            -url - input url from console
        :Return:
            None
        """
        self.input_url = url


    def parse_html(self):
        """Method for parsing html of input url
        :Parameters:

        :Return:
            list of found urls
        """
        links = []
        page = requests.get(self.input_url)
        tree = html.fromstring(page.content)
        links.extend([link for link in tree.xpath('//a/@href') if '://www.' in link\
                     or 'mailto:' in link])
        return links


    def extract_domain(self, url):
        """Method for getting domain name
        :Parameters:
            -url - url from page's urls
        :Return:
            domain name
        """
        return urlparse(url).netloc[4:]


    def resolve_domain(self, url):
        """Method for getting ip
        :Parameters:
            -url - url from page's urls
        :Return:
            ip
        """
        return socket.gethostbyname(url)


    def print_result(self, url, domain, ip):
        """Method for printing result
        :Parameters:
            -url - url from page's urls
            -domain - url's domain
            -ip - url's ip
        :Return:
            string "URL - domain - ip"
            example "http://www.bbc.co.uk - bbc.co.uk - 212.58.246.78"
        """
        print '{} - {} - {}'.format(url, domain, ip)


    def main(self):
        """Main class method"""
        parsed_urls = self.parse_html()
        for url in parsed_urls:
            self.print_result(url, self.extract_domain(url),
                              self.resolve_domain(self.extract_domain(url)))


def main(urls_list):
    """Main script function """
    for url in urls_list:
        Crawler(url).main()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

