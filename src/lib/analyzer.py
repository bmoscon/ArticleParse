#!/usr/bin/python

from htmlparse import HtmlParse
import operator
import re

class Section(object):
    def __init__(self, text, length = None, anchor = 0):
        self.text = text
        if length:
            self.length = length
        else:
            self.length = len(text)
        self.anchors = anchor

    def txt(self):
        return self.text

    def len(self):
        return self.length

    def anchor_count(self):
        return self.anchors


class Analyzer(object):
    def __init__(self, url = None, content = None):
        if url:
            self.parser = HtmlParse(url = url)
        elif content:
            self.parser = HtmlParse(content = content)
        else:
            raise TypeError("must supply a URL or HTML content")

        self.sections = []

    # threshold is the minimum length section to consider
    def parse_sections(self, threshold = 25):
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
                # get anchor count for the section
                anchors = item.count("<a>")
                # once we have counted them, we can strip them too
                item = re.sub(r"</?a.*?>", " ", item)
                length = len(item)
                if length > threshold:
                    # it meets the threshold, add a new section
                    self.sections.append(Section(item, length, anchors))
                                     
                
    # threshold = minimum size compared to the biggest section size
    # if the largest section is 5000 characters, and the threshold is 50.0,
    # only sections with a size that are at least 2500 characters (50% of largest
    # section size) will be retained
    def get_main_sections(self, threshold = 25.0):
        # sort by length, then reverse so we are sorted in descending order
        self.sections.sort(key = operator.attrgetter('length'))
        self.sections.reverse()
        
        base = self.sections[0].len();
        base_anchor = self.sections[0].anchor_count()
        
        ret = []

        for section in self.sections:
            section_length = section.len()
            percentage = float(section_length) / float(base) * 100.0
            anchor_delta = abs(base_anchor - section.anchor_count())
            if percentage >= threshold:
                # to do - something meaninful here
                if anchor_delta < 20:
                    ret.append(section.txt())
            else:
                # since we are sorted, once we are failing the threshold test
                # we can bail
                break

        return ret
