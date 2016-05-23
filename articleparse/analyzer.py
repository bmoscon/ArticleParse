"""
Copyright (C) 2013-2016  Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions 
associated with this software.
"""

from articleparse.htmlparse import HtmlParse
import re
from articleparse.stopwords import StopWords


'''
These are values that each section
must calculate and the values for which the 
analyzer must define thresholds
'''
ANCHOR_DENSITY = 'anchor_density'
ANCHOR_COUNT = 'anchor_count'
WORD_COUNT = 'word_count'
UPPER_COUNT = 'upper_count'
AVG_WORD_LEN = 'avg_word_len'
SENTENCE_COUNT = 'sentence_count'
AVG_SENTENCE_LEN = 'avg_sentence_len'
STOP_WORD_DENSITY = 'stop_word_density'


def lt(value, threshold):
    return value < threshold

def gt(value, threshold):
    return value > threshold

def bt(value, threshold):
    return value > threshold[0] and value < threshold[1]

def in_range(value, threshold, margin):
    '''
    Determine if a value is within a margin of error
    for a given threshold.
    '''
    if margin == 0:
        return False
    if hasattr(threshold, '__iter__'):
        for t in threshold:
            if value < (t + t*margin) and value > (t - t*margin):
                return True
        return False
    else:
        return value < (threshold + threshold*margin) and value > (threshold - threshold*margin)


class Section(object):
    '''
    A section of an article as demarcated by HTML tags (div, span, etc). 
    Contains only text, punctuation and HTML anchors
    '''
    def __init__(self, sec, position):
        self.pos = position
        self.__anchor_analysis(sec)
        self.length = len(self.text)
        self.__word_analysis()
        self.__sentence_analysis()

    def txt(self):
        return self.text

    def len(self):
        return self.length

    def position(self):
        return self.pos

    def access(self, member):
        if member == UPPER_COUNT:
            return self.upper_count
        if member == ANCHOR_COUNT:
            return self.anchor_count
        if member == ANCHOR_DENSITY:
            return self.anchor_density
        if member == WORD_COUNT:
            return self.word_count
        if member == AVG_WORD_LEN:
            return self.avg_word_len
        if member == SENTENCE_COUNT:
            return self.sentence_count
        if member == AVG_SENTENCE_LEN:
            return self.avg_sentence_len
        if member == STOP_WORD_DENSITY:
            return self.stop_word_density
        else:
            raise TypeError("Bad Member")

    def __anchor_analysis(self, sec):
        '''
        Performs analysis of the anchors in the section.
        Computes:
        * Count
        * Density
        '''
        anchor_lengths = 0
        anchor_texts = re.findall(r"<a.*?>(.*?)</a>", sec, re.IGNORECASE)
        anchors = len(anchor_texts)
        anchor_lengths = sum(len(element) for element in anchor_texts)
            
        # once we have counted them, we can strip them too
        sec = re.sub(r"</?a.*?>", " ", sec)
        length = len(sec)
            
        # calculate anchor density
        density = 0 if length == 0 else float(anchor_lengths) / float(length)


        self.anchor_count = anchors
        self.anchor_density = density
        self.text = sec

    def __word_analysis(self):
        '''
        Analysis of words in the section's text.
        Computes:
        * Word count
        * Average word length
        * Uppercase word count
        * Stop word density
        '''

        words = self.text
        words = re.sub(r"[^\w\s]", "", words)
        words = words.split()

        upper_count = 0
        total_len = 0
        num_words = len(words)

        total_len = sum(len(word) for word in words)
        upper_count = sum(1 if word[0].isupper() else 0 for word in words)
        
        avg_len = 0 if num_words == 0 else float(total_len) / float(num_words)

        self.word_count = num_words
        self.avg_word_len = avg_len
        self.upper_count = upper_count
        
        num_stop_words = sum(1 if StopWords.is_stop_word(word) else 0 for word in words)
        self.stop_word_density = 0 if num_words == 0 else float(num_stop_words / num_words)

    def __sentence_analysis(self):
        '''
        Sentence analysis. 
        Computes:
        * Number of sentences
        * Average sentence length (in terms of characters, not words)
        '''
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

        self.sentence_count = num_sentences
        self.avg_sentence_len = avg_len


class Analyzer(object):
    def __init__(self, url = None, content = None, fp = None):
        self.parser = HtmlParse(url=url, content=content, fp=fp)
        self.parser.remove_non_html()
        self.sections = []
        
        '''
        for each text feature, specify a threshold, a comparison, and a range
        example: 'word_count': [50, '>', 0.1] means that any word count less than 50 is considered
        to be boiler plate, anything greater than 50 is content. The range is a percentage 
        meaning that anything within 10% of the threshold (so in this case +- 5 is the range 
        45 to 55 inclusive) gets a partial point. A range of 0 means to ignore the range 
        and not assign partial points
        '''
        self.classification = {ANCHOR_DENSITY: [0.333, lt, 0.1],
                               WORD_COUNT: [40, gt, 0.1],
                               STOP_WORD_DENSITY: [[.30, .566], bt, 0.02]
                               }
        


    # Parse the HTML into sections
    # these are stored in the list, self.sections
    # 
    # threshold: integer value that specifies the minimum length of a section
    #
    # returns: nothing
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


    # determine how likely the section is to be a 'main' section,
    # that is, one with article content. This is done by comparing
    # different features of the text and calculating points for each
    # feature. Total points correlates with the probability that the
    # section is a main section. Low points = boiler plate,
    # high points = content
    #
    # Sections are evaluated in order of their appearance in the HTML since the page layout
    # is significant in determining if a section is boilerplate or content
    #
    # curr: current Section object
    #
    # returns: points and points possible, both floats
    def __classifier(self, curr):
        score = 0.0
        points_possible = 0.0
        for key, value in self.classification.items():
            points_possible += 1.0
            attribute = curr.access(key)
            threshold, comparator, margin = value
           
            if in_range(attribute, threshold, margin):
                # we are witin the range of partial points
                score += 0.5
            elif comparator(attribute, threshold):
                score += 1.0
        return score, points_possible
    
    
    # Since section ordering is significant, this classifier uses ordering
    # metrics to determine if the section is boilerplate or content
    #
    # curr, prev, next_sec: current, previous and next Sections
    #
    # returns: a float with the score of the section 
    def __neighbor_classifier(self, curr, prev, next_sec):
        return 0.0, 0.0

    '''           
    def __word_feature_classifier(self, prev, curr, next_sec):
        if curr.anchor_density() > 0.333:
            return False
        if prev.anchor_density() > 0.555:
            if curr.word_count() > 40:
                return True
            elif next_sec.word_count() > 17:
                return True
            else:
                return False
        else:
            if curr.word_count() > 16:
                return True
            elif next_sec.word_count() > 15:
                return True
            elif prev.word_count() > 4:
                return True
            else:
                return False
    '''
    
    # For each section, call the individual classifier and the
    # neighbor classifier. 
    #
    # returns: list of dictionaries. each dict contains the probability that the text is
    # content and the text
    def analyze_sections(self):
        ret = []

        for i in range(0, len(self.sections)):
            score1, pp1 = self.__classifier(self.sections[i])
            score2, pp2 = self.__neighbor_classifier(self.sections[i], 
                                                     self.sections[i-1] if i > 0 else None, 
                                                     self.sections[i+1] if i+1 < len(self.sections) else None)
            score = (score1 + score2) / (pp1 + pp2)
            ret.append({'probability':score, 'content':self.sections[i].txt()})

        return ret
            
            
