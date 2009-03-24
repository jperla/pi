# coding=utf-8

import os
import re
import urllib
import urllib2
import cookielib
import waiter

#session object 
class Session(object):
    def __init__(self):
        self._cookie_jar = cookielib.CookieJar()

    @property
    def cookie_processor(self):
        return urllib2.HTTPCookieProcessor( self._cookie_jar)

            
class Spider(waiter.Waiter):
    def __init__(self, session=None):
        waiter.Waiter.__init__(self)
        self._session = session
        self._user_agent = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.4)  Gecko/20061201 Firefox/2.0.0.4 (Ubuntu-feisty)'
        
    def _create_opener(self):
        if self._session is None:
            return urllib2.build_opener()
        else:
            return urllib2.build_opener(self._session.cookie_processor)

    def _create_request(self, url, data):
        if data is None:
            request = urllib2.Request(url)
        else:
            request = urllib2.Request(url, urllib.urlencode(data))
        request.add_header('User-Agent', self._user_agent)
        return request

    def get(self, url, data=None):
        """
        >>> s = Spider()
        >>> html = s.get('http://www.google.com/')
        >>> html.startswith('<html><head>')
        True
        """
        request = self._create_request(url, data)
        opener = self._create_opener()
        html = None
        try: 
            return opener.open(request).read()
        except:
            #try once again
            try:
                return opener.open(request).read()
            except Exception, e:
                raise Exception('Could not open page, tried twice', e)

    @staticmethod
    def get_matches(html, regex):
        """
        >>> html = '<html><head></head><body>This is a test html.</body></head>'
        >>> print Spider.get_matches(html, '<(.*?)>')
        ['html', 'head', '/head', 'body', '/body', '/head']
        """
        p = re.compile(regex, re.M | re.S)
        return p.findall(html)

    @staticmethod
    def get_match(html, regex):
        """
        >>> html = '<html><head></head><body>This is a test html.</body></head>'
        >>> print Spider.get_match(html, ' is(.*)test')
         a 
        >>> print Spider.get_match(html, 'ody>(.*)</bod')
        This is a test html.
        >>> print Spider.get_match(html, 'Th(.*?)s')
        i
        >>> print Spider.get_match(html, 'Th(.*)s')
        is is a te
        """
        matches = Spider.get_matches(html, regex)
        return matches[0] if len(matches) > 0 else None

    @staticmethod
    def finds_match(html, regex):
        """
        >>> html = '<html><head></head><body>This is a test html.</body></head>'
        >>> print Spider.finds_match(html, ' is(.*)test')
        True
        >>> print Spider.finds_match(html, 'ody>(.*)</bod')
        True
        >>> print Spider.finds_match(html, 'nothing')
        False
        >>> print Spider.finds_match(html, 'That')
        False
        """
        matches = Spider.get_matches(html, regex)
        if len(matches) == 0:
            return False
        else:
            return True

    def get_matches_in_url(self, url, regex):
        html = self.get(url)
        return self.get_matches(html, regex)

    def get_match_in_url(self, url, regex):
        html = self.get(url)
        return self.get_match(html, regex)

    @staticmethod
    def clean_html_entities(html):
        #http://www.asciitable.com/
        #http://www.w3schools.com/tags/ref_entities.asp

        # ISO 8859-1 Character Entities
        char_maps = {
            'À' : "&Agrave;", 'Á' : "&Aacute;", 'Â' : "&Acirc;", 
            'Ã' : "&Atilde;", 'Ä' : "&Auml;", 'Å' : "&Aring;",
            'Æ' : "&AElig;", 'Ç' : "&Ccedil;",
            'È' : "&Egrave;", 'É' : "&Eacute;", 'Ê' : "&Ecirc;", 'Ë' : "&Euml;",
            'Ì' : "&Igrave;", 'Í' : "&Iacute;", 'Î' : "&Icirc;", 'Ï' : "&Iuml;",
            'Ð' : "&ETH;", 'Ñ' : "&Ntilde;",
            'Ò' : "&Ograve;", 'Ó' : "&Oacute;", 'Ô' : "&Ocirc;", 
            'Õ' : "&Otilde;", 'Ö' : "&Ouml;", 'Ø' : "&Oslash;",
            'Ù' : "&Ugrave;", 'Ú' : "&Uacute;", 'Û' : "&Ucirc;", 'Ü' : "&Uuml;",
            'Ý' : "&Yacute;",
            'Þ' : "&THORN;", 'ß' : "&szlig;",
            'à' : "&agrave;", 'á' : "&aacute;", 'â' : "&acirc;", 
            'ã' : "&atilde;", 'ä' : "&auml;", 'å' : "&aring;",
            'æ' : "&aelig;", 'ç' : "&ccedil;",
            'è' : "&egrave;", 'é' : "&eacute;", 'ê' : "&ecirc;", 'ë' : "&euml;",
            'ì' : "&igrave;", 'í' : "&iacute;", 'î' : "&icirc;", 'ï' : "&iuml;",
            'ð' : "&eth;", 'ñ' : "&ntilde;",
            'ò' : "&ograve;", 'ó' : "&oacute;", 'ô' : "&ocirc;", 
            'õ' : "&otilde;", 'ö' : "&ouml;", 'ø' : "&oslash;",
            'ù' : "&ugrave;", 'ú' : "&uacute;", 'û' : "&ucirc;", 'ü' : "&uuml;",
            'ý' : "&yacute;", 'þ' : "&thorn;", 'ÿ' : "&yuml;", 
            '&' : '&amp;', "'" : '&#039;', '"' : '&quot;', };

        for char in char_maps.keys():
            html = html.replace(char_maps[char], char)
        return html

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()



