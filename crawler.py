import re
import sys
import socket
from lxml import html
import requests


class Crawler(object):
    """Class for getting iformation about
    all url's domain and ip that are in web page """

    def __init__(self, urls):
        """Crawler's init method
        :Parameters:
            urls - input urls from console
        """
        self.input_urls = urls
        self.result = {}

    def __parse_html(self, url):
        """Method for parsing html of input url
        :Parameters:
            url - url from user's input
        :Return:
            list of all parsed links
        """
        try:
            page = requests.get(url)
        except requests.exceptions.ConnectionError as err:
            print '{} address is not valid'.format(url)
            print '---------------------------------------'
        tree = html.fromstring(page.content)
        parsed_links = [link for link in tree.xpath('//@href')\
                                   if 'http' in link or 'mailto:' in link]
        return parsed_links

    def __resolve_url(self, url):
        """Method for getting domain and ip
        from parsed url
        :Parameters:
            url - url from parsed html
        :Return:
            list which contain url, url's domain
            and url's ip
        """
        domain = re.search(r'(//([^/?#]*))', url).group()[2:]
        try:
            ip = socket.gethostbyname(domain)
        except socket.error:
            ip = None
        return [url, domain, ip]

    def print_result(self):
        """Method for printing result
           example: "http://www.bbc.com : http://www.bbc.co.uk/news/
           - bbc.co.uk - 212.58.246.78"
        """
        for key,result in self.result.items():
            for res in result:
                print '{} : {} - {} - {}'.format(key, *res)

    def run(self):
        """Main class method
        :Return:
            result list
        """
        for url in self.input_urls:
            links = self.__parse_html(url)
            self.result[url] = []
            for link in links:
                self.result[url].append(self.__resolve_url(link))
        return self.result


if __name__ == '__main__':
    crawler = Crawler(sys.argv[1:])
    crawler.run()
    crawler.print_result()

