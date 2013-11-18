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
    def __init__(self, sec, position):
        self.pos = position
        # incoming section data should still have the anchor tags
        # so lets parse those out first
        self.__anchor_analysis(sec)
        self.length = len(self.text)
        self.__word_analysis()
        self.__sentence_analysis()


    # returns number of anchors and anchor density (length of anchors / length of section) 
    def __anchor_analysis(self, sec):
        # calculate length of each anchor (text between <a></a> tags)
        anchor_lengths = 0
        anchor_texts = re.findall(r"<a.*?>(.*?)</a>", sec, re.IGNORECASE)
        anchors = len(anchor_texts)
        for element in anchor_texts:
            anchor_lengths += len(element)
            
        # once we have counted them, we can strip them too
        sec = re.sub(r"</?a.*?>", " ", sec)
        length = len(sec)
            
        # calculate anchor density
        try:
            density = float(anchor_lengths) / float(length)
        except:
            density = 0

        self.a_count = anchors
        self.a_density = density
        self.text = sec
        

    # returns number of words and avg word length
    def __word_analysis(self):
        words = self.text
        words = re.sub(r"[^\w\s]", "", words)
        words = words.split()

        upper_count = 0
        total_len = 0
        num_words = len(words)

        for word in words:
            total_len += len(word)
            if word[0].isupper():
                upper_count += 1
        
        try:
            avg_len = float(total_len) / float(num_words)
        except:
            avg_len = 0

        self.w_count = num_words
        self.avg_w_len = avg_len
        self.u_count = upper_count


    # returns number of sentences and avg sentence length
    def __sentence_analysis(self):
        sentences = self.text
        sentences = re.sub(r"[?!]", ".", sentences)
        # most all sentences' periods are followed by a space
        # not guaranteed, but vast majority are. if we dont do this
        # things like abbreviations and numerical information will 
        # create fake sentence divisions
        sentences = sentences.split(". ")

        num_sentences = len(sentences)
        total_len = 0

        for sentence in sentences:
            total_len += len(sentence)

        try:
            avg_len = float(total_len) / float(num_sentences)
        except:
            avg_len = 0

        self.s_count = num_sentences
        self.avg_s_len = avg_len


    ####################
    #                  #
    # Accessor Methods #
    #                  #
    ####################

    def txt(self):
        return self.text

    def len(self):
        return self.length

    def position(self):
        return self.pos
        
    def upper_count(self):
        return self.u_count

    def anchor_count(self):
        return self.a_count

    def anchor_density(self):
        return self.a_density

    def word_count(self):
        return self.w_count

    def avg_word_len(self):
        return self.avg_w_len

    def sentence_count(self):
        return self.s_count

    def avg_sentence_len(self):
        return self.avg_s_len


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

        position = 0
        for item in html:
            if len(item) > 1:
                sec = Section(item, position)
                if sec.len() > threshold:
                    self.sections.append(sec)
            position += 1

                
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
