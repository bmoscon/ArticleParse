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


class StopWords(object):
    # Stop words list
    stop_words = set(["a",
                      "about",
                      "able"
                      "above",
                      "across",
                      "after",
                      "afterwards",
                      "again",
                      "against",
                      "all",
                      "almost",
                      "alone",
                      "along",
                      "already",
                      "also",
                      "although",
                      "among",
                      "am",
                      "an",
                      "and",
                      "any",
                      "are",
                      "as",
                      "at",
                      "be",
                      "because",
                      "been",
                      "but",
                      "by",
                      "can",
                      "cannot",
                      "could",
                      "dear",
                      "did",
                      "do",
                      "does",
                      "either",
                      "else",
                      "ever",
                      "every",
                      "for",
                      "from",
                      "get",
                      "got",
                      "had",
                      "has",
                      "have",
                      "he",
                      "her",
                      "hers",
                      "him",
                      "his",
                      "how",
                      "however",
                      "i",
                      "if",
                      "in",
                      "into",
                      "is",
                      "it",
                      "its",
                      "just",
                      "least",
                      "let",
                      "like",
                      "likely",
                      "may",
                      "me",
                      "might",
                      "most",
                      "must",
                      "my",
                      "neither",
                      "no",
                      "nor",
                      "not",
                      "of",
                      "off",
                      "often",
                      "on",
                      "only",
                      "or",
                      "other",
                      "our",
                      "own",
                      "rather",
                      "said",
                      "say",
                      "says",
                      "she",
                      "should",
                      "since",
                      "so",
                      "some",
                      "than",
                      "that",
                      "the",
                      "their",
                      "them",
                      "then",
                      "there",
                      "these",
                      "they",
                      "this",
                      "tis",
                      "to",
                      "too",
                      "twas",
                      "us",
                      "wants",
                      "was",
                      "we",
                      "were",
                      "what",
                      "when",
                      "where",
                      "which",
                      "while",
                      "who",
                      "whom",
                      "why",
                      "will",
                      "with",
                      "would",
                      "yet",
                      "you",
                      "your"
                      ])
    @staticmethod
    def is_stop_word(word):
        return word.lower() in StopWords.stop_words
