# Simple negation detector

This repository contains scripts to detect negations in Dutch and English.

## Requirements & setup
This script has been tested with Python 3.5, but it should work with Python 2.7 as well.
Installation is slightly different, as you need to make sure you have the right version
of `treetagger-python`.

1. Install [Treetagger](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/).
2. Install the NLTK. Be sure to also download the pre-trained tokenizers.
   `import nltk`, followed by `nltk.download('all')` should work, but you can also manually select what you want to install.
3. Install [treetagger-python](https://github.com/miotto/treetagger-python).

## Using the negation detector

```python
from negation_detector import NegationDetector
nd = NegationDetector('english') # or 'spanish' or 'dutch'.

# See whether the word is a negation, and if so: what kind.
neg, kind = nd.negation_status('no')

# Analyze a sentence.
analyzed_sentence = nd.check_sentence("I don't like spam.")

# Analyze a text
# Doesn't work well with newlines, so split the text into paragraphs using text.split('\n')
# and check paragraph by paragraph.
analyzed_text = nd.check_text("I don't like spam. It is not something I like.")
```
