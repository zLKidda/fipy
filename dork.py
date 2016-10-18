import urlparse, urllib2, traceback, re
urllib2.socket.setdefaulttimeout(5.0)

DEBUG = 0

class Dorker(object):
    def __init__(self, engine='duck'):
        self._engine = engine
        self.search_engines = [] # available dorking search engines
        self.search_engines.append('duck')
        self.search_engines.append('bing')
        self.search_engines.append('google')
        self.search_engines.append('yahoo')
        self.search_engines.append('yandex')

    def dork(self, search):
        """
        Perform a search and return links.
        Use -duck- engine by default.
        """
        if self._engine == 'duck' or not self._engine: # seems hopeless at 20-02-2011 -> 19-02-2016
            search_url = "https://duckduckgo.com/html/?q=" + '"' + urllib2.quote(search) + '"'

        elif self._engine == 'bing': # works at 20-02-2011 -> 19-02-2016
            search_url = "https://www.bing.com/search?q=" + 'instreamset:(url):"' + urllib2.quote(search) + '"'

        elif self._engine == 'google': # works at 11/11/2011 -> 26-02-2016
            search_url = "https://www.google.com/xhtml?q=" + 'inurl:"' + urllib2.quote(search) + '"'

        elif self._engine == 'yahoo': # works at 20-02-2011 -> 19-02-2016
            search_url = "https://search.yahoo.com/search?q=" + 'instreamset:(url):"' + urllib2.quote(search) + '"'

        elif self._engine == 'yandex': # works at 20-02-2011 -> 19-02-2016
            search_url = "https://yandex.ru/search/?text=" + 'inurl:"' + urllib2.quote(search) + '"'
        else:
            print "\n[Error] This search engine is not supported!\n" 
            print "[Info] List of available:"
            print '-'*25
            for e in self.search_engines:
                print "+ "+e
            print ""
        try:
            self.search_url = search_url
            #print "\n[Info] Search query:", search_url
            if search_url.startswith("https"):
                proxy = urllib2.ProxyHandler({'http': '127.0.0.1'})
                opener = urllib2.build_opener(proxy)
                urllib2.install_opener(opener)
                url = urllib2.urlopen(urllib2.Request(search_url,
                                      headers={'User-Agent':"Googlebot/2.1b"}))
            else:
                url = urllib2.urlopen(urllib2.Request(search_url,
                                      headers={'User-Agent':"Googlebot/2.1b"}))
	except urllib2.URLError, e:
            if DEBUG:
                traceback.print_exc()
            print "\n[Error] Cannot connect!"
            exit()
        html_data = url.read()
        if self._engine == 'duck':
            regex = '<a rel="nofollow" class="large" href="(.+?)"' # regex magics 20-02/2016
        if self._engine == 'bing':
            regex = '<li class="b_algo"><h2><a href="(.+?)">' # regex magics 20-02/2016
        if self._engine == 'google':
            regex = '<h3 class="r"><a href="/url(.+?)">' # regex magics 20-02/2016
        if self._engine == 'yahoo':
            regex = '<h3 class="title"><a class=" ac-algo ac-21th lh-15" href="(.+?)">' # regex magics 20-02/2016
        if self._engine == 'yandex':
            regex = '<a class="link serp-item__title-link" target="_blank" href="(.+?)"' # regex magics 20-02/2016
        pattern = re.compile(regex)
        links = re.findall(pattern, html_data)

        found_links = []
        if links:
            for link in links:
                link = urllib2.unquote(link)
                if self._engine == 'bing':
                    link = link.rsplit('" h=',1)[0]
                if self._engine == "google":
                    link = link.rsplit('&amp;sa',1)[0]
                    if link.startswith("?q="):
                        link = link.replace("?q=","")
                if self._engine == "yahoo":
                    link = link.rsplit('" target=',1)[0]
                found_links.append(link)
        return found_links

if __name__ == '__main__':
    testVar = raw_input("Enter the google dork:")
    for a in ['bing', 'yahoo', 'duck']:
	dork = Dorker(a)
        res = dork.dork(testVar)
        if res:
            for b in res:
                print b
		f = open('workfile.txt', 'a')
		f.write(str(b)+ '\n')
