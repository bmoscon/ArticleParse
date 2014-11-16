"""
Copyright (C) 2013-2014  Bryant Moscon - bmoscon@gmail.com
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to 
 deal in the Software without restriction, including without limitation the 
 rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 sell copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 1. Redistributions of source code must retain the above copyright notice, 
    this list of conditions, and the following disclaimer.

 2. Redistributions in binary form must reproduce the above copyright notice, 
    this list of conditions and the following disclaimer in the documentation 
    and/or other materials provided with the distribution, and in the same 
    place and form as other copyright, license and disclaimer information.

 3. The end-user documentation included with the redistribution, if any, must 
    include the following acknowledgment: "This product includes software 
    developed by Bryant Moscon (http://www.bryantmoscon.org/)", in the same 
    place and form as other third-party acknowledgments. Alternately, this 
    acknowledgment may appear in the software itself, in the same form and 
    location as other such third-party acknowledgments.

 4. Except as contained in this notice, the name of the author, Bryant Moscon,
    shall not be used in advertising or otherwise to promote the sale, use or 
    other dealings in this Software without prior written authorization from 
    the author.


 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
 THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
 THE SOFTWARE.
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
        # remove linebreaks
        self.parsed = re.sub(r"\n+", "", self.parsed)
        self.parsed = re.sub(r"\r+", "", self.parsed)
        self.parsed = re.sub(r"&#13;", "", self.parsed)

        # remove scripts, stylesheets, and comments
        self.parsed = re.sub(r"<!--.*?-->", "", self.parsed)
        self.parsed = re.sub(r"<(style).*?</\1>(?s)", "", self.parsed)
        self.parsed = re.sub(r"<(script).*?</\1>(?s)", " ", self.parsed)


    # remove everything not included in the <body></body> tags
    def isolate_body(self):
        body_start = self.parsed.find("<body")
        body_start = self.parsed.find(">", body_start)
        
        body_end = self.parsed.find("</body")
        
        self.parsed = self.parsed[body_start+1:body_end]


    # remove all HTML tags.
    # optionally retain the tags listed in retain_list
    def strip(self, retain_list = []):
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
        
        self.parsed = re.sub(r"&#0*9;", " ", self.parsed)
        self.parsed = re.sub(r"&tab;", " ", self.parsed)
        
        self.parsed = re.sub(r"&#201;", "e", self.parsed)
        self.parsed = re.sub(r"&Eacute;", "e", self.parsed)
        self.parsed = re.sub(r"&#233;", "e", self.parsed)
        self.parsed = re.sub(r"&eacute;", "e", self.parsed)
        
        

    # converts tags of one type to another
    # convert_list is the list of tags to convert to  and from
    # example: ["a", "b", "/a", "/b"] will convert <a> to <b> and </a> to </b>
    def convert(self, c_list):
        for i in range(0, len(c_list), 2):
            self.parsed = re.sub(r"<%s.*?>" %c_list[i], "<"+c_list[i + 1]+">", self.parsed)
           
            
    # returns the parsed HTML     
    def get_parsed(self):
        return self.parsed


    # returns the original HTML
    def get_html(self):
        return self.html


    # resets the parsed HTML back to the original
    def reset(self):
        self.parsed = self.html
