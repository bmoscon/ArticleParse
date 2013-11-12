"""
Copyright (C) 2013  Bryant Moscon - bmoscon@gmail.com
 
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

from htmlparse import HtmlParse
import operator
import re

class Section(object):
    def __init__(self, text, length, anchor, density):
        self.text = text
        self.length = length
        self.anchors = anchor
        self.density = density

    def txt(self):
        return self.text

    def len(self):
        return self.length

    def anchor_count(self):
        return self.anchors

    def anchor_density(self):
        return self.density


class Analyzer(object):
    def __init__(self, url = None, content = None, fp = None):
        if url:
            self.parser = HtmlParse(url = url)
        elif content:
            self.parser = HtmlParse(content = content)
        elif fp:
            self.parser = HtmlParse(fp = fp)
        else:
            raise TypeError("must supply a URL, File, or HTML content")

        self.sections = []

    # threshold is the minimum length section to consider
    def parse_sections(self, threshold):
        self.parser.isolate_body()
        # retain these tags for analysis
        self.parser.strip(retain_list = ["div", "/div", "span", "/span", "a", "/a"])
        # convert spans to div, since they play the same role in our analysis
        self.parser.convert(["span", "div", "/span", "/div"])
        self.parser.decode_entities()

        html = self.parser.get_parsed()

        # find all sections enclosed by <div> tags
        html = re.split("</?div>", html)

        for item in html:
            if len(item) > 0:
                # calculate length of each anchor (text between <a></a> tags)
                anchor_lengths = 0
                anchor_texts = re.findall(r"<a.*?>(.*?)</a>", item, re.IGNORECASE)
                anchors = len(anchor_texts)
                for element in anchor_texts:
                    anchor_lengths += len(element)
                
                # once we have counted them, we can strip them too
                item = re.sub(r"</?a.*?>", " ", item)
                length = len(item)

                # calculate anchor density
                density = float(anchor_lengths) / float(length)

                if length > threshold:
                    # it meets the threshold, add a new section
                    self.sections.append(Section(item, length, anchors, density))
                                     
                
    # threshold = minimum size compared to the biggest section size
    # if the largest section is 5000 characters, and the threshold is 50.0,
    # only sections with a size that are at least 2500 characters (50% of largest
    # section size) will be retained
    def get_main_sections(self, threshold, density_threshold):
        # sort by length, then reverse so we are sorted in descending order
        self.sections.sort(key = operator.attrgetter('length'))
        self.sections.reverse()
        
        base = self.sections[0].len();
        base_anchor = self.sections[0].anchor_density()
        
        ret = []

        for section in self.sections:
            section_length = section.len()
            percentage = float(section_length) / float(base) * 100.0
            anchor_delta = abs(base_anchor - section.anchor_density())
            if percentage >= threshold:
                # excludes sections with anchor densities that differ by more than
                # density_threshold from the base section. Reasoning is that the navigation 
                # sections at the top and bottom of the page are typically long in length 
                # (and would not be excluded due to the other thresholds) 
                # but have very high link densities 
                if anchor_delta < density_threshold:
                    ret.append(section.txt())
            else:
                # since we are sorted, once we are failing the threshold test
                # we can bail
                break

        return ret
