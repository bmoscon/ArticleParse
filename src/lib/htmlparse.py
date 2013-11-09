#!/usr/bin/python

import re
import urllib


class HtmlParse(object):
    def __init__(self, url = None, content = None, initial_parse = True):
        if url:
            self.html = urllib.urlopen(url).read()
        elif content:
            self.html = content
        else:
            raise TypeError("must supply a URL or HTML content")

        self.parsed = self.html

        # perform initial parsing
        if initial_parse:
            self.__initial_parse()


    def __initial_parse(self):
        # remove linebreaks
        self.parsed = re.sub(r"\n+", "", self.parsed)
        self.parsed = re.sub(r"\r+", "", self.parsed)

        # remove scripts, stylesheets, and comments
        self.parsed = re.sub(r"<!--.*?-->", "", self.parsed)
        self.parsed = re.sub(r"<(style).*?</\1>(?s)", "", self.parsed)
        self.parsed = re.sub(r"<(script).*?</\1>(?s)", " ", self.parsed)

    def __consolidate_spacing(self):
        self.parsed = re.sub(r"\s+", " ", self.parsed)

    # remove everything not included in the <body></body> tags
    def isolate_body(self):
        body_start = self.parsed.find("<body")
        body_start = self.parsed.find(">", body_start)
        
        body_end = self.parsed.find("</body")
        
        self.parsed = self.parsed[body_start+1:body_end]

    def strip(self, retain_list = []):
        # convert tags we want to retain
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

        self.__consolidate_spacing()

        
    # removes HTML entities. Obviously this is far from complete
    def decode_entities(self):
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
        

    # converts tags of one type to another
    # convert_list is the list of tags to convert to  and from
    # example: ["a", "b", "/a", "/b"] will convert <a> to <b> and </a> to </b>
    def convert(self, convert_list):
        i = 0
        while i < len(convert_list):
            self.parsed = re.sub(r"<%s.*?>" %convert_list[i], convert_list[i + 1], self.parsed)
            i += 2
            
        
    def get_parsed(self):
        return self.parsed

    def get_html(self):
        return self.html

    def reset(self):
        self.parsed = self.html
