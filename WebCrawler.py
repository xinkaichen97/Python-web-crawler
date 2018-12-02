# encoding=utf-8
from bs4 import BeautifulSoup
import socket
import urllib2
import re

urls = raw_input('Welcome!\nEnter URL to crawl: ')  #input the URL
count = int(raw_input('Max Count [e.g. 100]: '))  #input the maximum number
flag = int(raw_input('Choose an algorithm [1.BFS  2.DFS]:'))  #indicate the preferred algorithm

class Crawler:
    def __init__(self, base_url):
        # Using base_url to initialize URL queue
        self.UrlSequence = UrlSequence()
        # Add base_url to the "unvisited" list
        self.UrlSequence.Unvisited_Add(base_url)
        print "Add the base url \"%s\" to the unvisited url list" % str(self.UrlSequence.unvisited)


    def crawling(self, base_url, max_count, flag):
        # Loop condition: the "unvisited" list is not empty & the number of visited URLs is not bigger than max_count
        while self.UrlSequence.UnvisitedIsEmpty() is False and self.UrlSequence.Visited_Count() <= max_count:
            # Dequeue or pop, according to the flag
            if flag == 1:  # using BFS
                visitUrl = self.UrlSequence.Unvisited_Dequeue()
            else:  # using DFS
                visitUrl = self.UrlSequence.Unvisited_Pop()
            print "Pop out one url \"%s\" from unvisited url list" % visitUrl
            if visitUrl in self.UrlSequence.visited or visitUrl is None or visitUrl == "":
                continue
            # Get the links
            links = self.getLinks(visitUrl)
            print "Get %d new links" % len(links)
            # Now "visitUrl" has been visited. Add it to the "visited" list
            self.UrlSequence.Visited_Add(visitUrl)
            print "Visited url count: " + str(self.UrlSequence.Visited_Count())
            # Add the unvisited URL to the "unvisited" list
            for link in links:
                self.UrlSequence.Unvisited_Add(link)
            print "%d unvisited links:" % len(self.UrlSequence.getUnvisitedUrl())

    # Get links from the source code
    def getLinks(self, url):
        links = []
        data = self.getPageSource(url)
        if data[0] == "200":
            # Create a BeautifulSoup object
            soup = BeautifulSoup(data[1])
            # Find all HTML sentences <a href=".*">
            # .* is a regular expression meaning getting the content between quotation marks(""), i.e. the URLs
            a = soup.findAll("a", {"href": re.compile(".*")})
            for i in a:
                if i["href"].find("http://") != -1 or i["href"].find("https://") != -1:
                    links.append(i["href"])
        return links

    # Get the page source code
    def getPageSource(self, url, timeout=100, coding=None):
        try:
            socket.setdefaulttimeout(timeout)
            req = urllib2.Request(url)
            # Add HTTP header
            req.add_header('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
            response = urllib2.urlopen(req)
            if coding is None:
                coding = response.headers.getparam("charset")
            if coding is None:
                page = response.read()
            else:
                page = response.read()
                page = page.decode(coding).encode('utf-8')
            # HTTP Status Code 200 means requests are accepted by the server
            return ["200", page]
        except Exception, e:
            print str(e)
            return [str(e), None]


class UrlSequence:
    def __init__(self):
        # the set of visited URLs
        self.visited = []
        # the set of unvisited URLs
        self.unvisited = []

    # get "visited" list
    def getVisitedUrl(self):
        return self.visited

    # get "unvisited" list
    def getUnvisitedUrl(self):
        return self.unvisited

    # Add to visited URLs
    def Visited_Add(self, url):
        self.visited.append(url)

    # Remove from visited URLs
    def Visited_Remove(self, url):
        self.visited.remove(url)

    # Dequeue from unvisited URLs
    def Unvisited_Dequeue(self):
        try:
            return self.unvisited.pop(0)
        except:
            return None

    # Pop from unvisited URLs
    def Unvisited_Pop(self):
        try:
            return self.unvisited.pop()
        except:
            return None

    # Add new URLs
    def Unvisited_Add(self, url):
        if url != "" and url not in self.visited and url not in self.unvisited:
            self.unvisited.append(url)

    # The count of visited URLs
    def Visited_Count(self):
        return len(self.visited)

    # The count of unvisited URLs
    def Unvisited_Count(self):
        return len(self.unvisited)

    # Determine whether "unvisited" queue is empty
    def UnvisitedIsEmpty(self):
        return len(self.unvisited) == 0


def main(base_url, max_count, flag):
    craw = Crawler(base_url)
    craw.crawling(base_url, max_count, flag)


if __name__ == "__main__":
    main(urls , count, flag)
    print "Mission accomplished! Thanks for using :)"