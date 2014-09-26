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

from htmlparse import HtmlParse
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
        anchor_lengths = sum(len(element) for element in anchor_texts)
            
        # once we have counted them, we can strip them too
        sec = re.sub(r"</?a.*?>", " ", sec)
        length = len(sec)
            
        # calculate anchor density
        density = 0 if length == 0 else float(anchor_lengths) / float(length)


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

        total_len = sum(len(word) for word in words)
        upper_count = sum(1 if word[0].isupper() else 0 for word in words)
        
        avg_len = 0 if num_words == 0 else float(total_len) / float(num_words)

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

        total_len = sum(len(sentence) for sentence in sentences)
        
        avg_len = 0 if num_sentences == 0 else float(total_len) / float(num_sentences)

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
        self.parser = HtmlParse(url=url, content=content, fp=fp)
        self.parser.remove_non_html()
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

               
    def __word_feature_classifier(self, prev, curr, next):
        if curr.anchor_density() > 0.333:
            return False
        if prev.anchor_density() > 0.555:
            if curr.word_count() > 40:
                return True
            elif next.word_count() > 17:
                return True
            else:
                return False
        else:
            if curr.word_count() > 16:
                return True
            elif next.word_count() > 15:
                return True
            elif prev.word_count() > 4:
                return True
            else:
                return False

        
    def get_main_sections(self):
        ret = []

        for i in range(0, len(self.sections)):
            curr = self.sections[i]
            if i == 0:
                prev = Section(" ", 0)
            else:
                prev = self.sections[i-1]
            
            if i == len(self.sections) - 1:
                next = Section(" ", 0)
            else:
                next = self.sections[i + 1]

            if self.__word_feature_classifier(prev, curr, next):
                ret.append(self.sections[i].txt())


        return ret
            
            
