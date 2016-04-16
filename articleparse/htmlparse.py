"""
Copyright (C) 2013-2014  Bryant Moscon - bmoscon@gmail.com
 
Please see the LICENSE file for the terms and conditions 
associated with this software.
"""

import re
import urllib.request as urllib


class HtmlParse(object):
    def __init__(self, url = None, content = None, fp = None):
        if content:
            self.html = content
        elif fp:
            with open(fp, "r") as f:
                self.html = f.read()
        elif url:
            self.html = urllib.urlopen(url).read().decode("UTF-8", errors='ignore')
        else:
            raise TypeError("must supply a URL, File, or HTML content")
            
        self.parsed = self.html

    def remove_non_html(self):
        '''
        removes linebreaks, javascript, css, comments, etc
        '''
        self.parsed = re.sub(r"\n+", "", self.parsed)
        self.parsed = re.sub(r"\r+", "", self.parsed)
        self.parsed = re.sub(r"&#13;", "", self.parsed)
        self.parsed = re.sub(r"<!--.*?-->", "", self.parsed)
        self.parsed = re.sub(r"<(style).*?</\1>(?s)", "", self.parsed)
        self.parsed = re.sub(r"<(script).*?</\1>(?s)", " ", self.parsed)

    def isolate_body(self):
        '''
        removes everything not enclosed in the body tags.
        this also removes the body tags
        '''
        body_start = self.parsed.find("<body")
        body_start = self.parsed.find(">", body_start)
        
        body_end = self.parsed.find("</body")
        
        self.parsed = self.parsed[body_start+1:body_end]

    def strip(self, retain_list = []):
        '''
        Removes all HTML tags except those specified in the retain list
        
        Parameters
        ----------
        retain_list: list of str
            The HTML tags specified in the retain list will not be stripped
        '''

        # convert retain list to placeholders
        lookup_table = []
        for tag in retain_list:
            replace = "&tag-" + tag + ";"
            lookup_table.append(replace)
            self.parsed = re.sub(r"<%s.*?>" %tag, replace, self.parsed)

        # remove all tags
        self.parsed = re.sub(r"<.*?>", " ", self.parsed)

        # convert retained tags back to originals
        for i in range(0, len(retain_list)):
            tag = "<" + retain_list[i] + ">"
            self.parsed = re.sub(r"%s" %lookup_table[i], tag, self.parsed)
        
        # condense all whitespace
        self.parsed = re.sub(r"\s+", " ", self.parsed)

    def decode_entities(self):
        '''
        remove HTML entities
        (incomplete)
        '''
        self.parsed = re.sub(r"&#0*34;", "\"", self.parsed)
        self.parsed = re.sub(r"&quot;", "\"", self.parsed)
        
        self.parsed = re.sub(r"&#0*39;", "'", self.parsed)
        self.parsed = re.sub(r"&apos;", "'", self.parsed)
        
        self.parsed = re.sub(r"&#0*38;", "&", self.parsed)
        self.parsed = re.sub(r"&amp;", "&", self.parsed)
        
        self.parsed = re.sub(r"&#0*60;", "<", self.parsed)
        self.parsed = re.sub(r"&lt;", "<", self.parsed)
        
        self.parsed = re.sub(r"&#0*62;", ">", self.parsed)
        self.parsed = re.sub(r"&gt;", ">", self.parsed)
        
        self.parsed = re.sub(r"&#160;", " ", self.parsed)
        self.parsed = re.sub(r"&nbsp;", " ", self.parsed)
        
        self.parsed = re.sub(r"&#169;", "Copyright", self.parsed)
        self.parsed = re.sub(r"&copy;", "Copyright", self.parsed)

        self.parsed = re.sub(r"&#8212;", "-", self.parsed)
        self.parsed = re.sub(r"&mdash;", "-", self.parsed)

        self.parsed = re.sub(r"&#8211;", "-", self.parsed)
        self.parsed = re.sub(r"&ndash;", "-", self.parsed)

        self.parsed = re.sub(r"&#8217;", "'", self.parsed)
        self.parsed = re.sub(r"&rsquo;", "'", self.parsed)

        self.parsed = re.sub(r"&#8220;", "\"", self.parsed)
        self.parsed = re.sub(r"&ldquo;", "\"", self.parsed)

        self.parsed = re.sub(r"&#8221;", "\"", self.parsed)
        self.parsed = re.sub(r"&rdquo;", "\"", self.parsed)
        
        self.parsed = re.sub(r"&#0*9;", " ", self.parsed)
        self.parsed = re.sub(r"&tab;", " ", self.parsed)
        
        self.parsed = re.sub(r"&#201;", "e", self.parsed)
        self.parsed = re.sub(r"&Eacute;", "e", self.parsed)
        self.parsed = re.sub(r"&#233;", "e", self.parsed)
        self.parsed = re.sub(r"&eacute;", "e", self.parsed)

    def convert(self, c_list):
        '''
        Convert tags of one type to another

        Parameters
        ----------
        c_list: list of str
            a conversion mapping
            example: ['a', 'b', '/a', '/b'] will convert <a> to <b> and </a> to </b>
        '''
        for i in range(0, len(c_list), 2):
            self.parsed = re.sub(r"<%s.*?>" %c_list[i], "<"+c_list[i + 1]+">", self.parsed)

    def get_parsed(self):
        return self.parsed

    def get_html(self):
        return self.html

    def reset(self):
        self.parsed = self.html
