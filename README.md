ArticleParse
============

[![License](https://img.shields.io/badge/license-XFree86-blue.svg)](LICENSE)


Library that strips boilerplate HTML from news articles and performs heuristic analysis to determine the body of the article. Ranks text sections of the website by probability of being news content.


Currently uses for analysis:

* Section Length
* Section Position
* Number of Anchors in a Section
* Anchor Density in a Section
* Word Count
* Uppercase Word Count
* Average Word Length
* Average Sentence Length
* Number of Sentences

This is a work in progress. I have manually tested it on several news websites, but extensive testing still needs to be performed.

Supports Python3
