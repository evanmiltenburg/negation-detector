from treetagger import TreeTagger
import nltk
import os
import json
from collections import namedtuple

Token = namedtuple('Token',['idx', 'word', 'pos', 'lemma', 'match', 'kind'])

class NegationDetector(object):
    """
    Class to detect negations for the following languages:
        * Dutch
        * English
        * Spanish
    """
    
    supported_languages = {'dutch', 'english', 'spanish'}
    
    def __init__(self, language):
        "Initialize NegationDetector with a specific language."
        self.this_dir, self.this_filename = os.path.split(__file__)
        self.language = language
        self._tokenizers = {'dutch': 'tokenizers/punkt/dutch.pickle',
                          'english': '',
                          'spanish': 'tokenizers/punkt/spanish.pickle'}
        self.json_files = {'english': 'english_negations.json'}
        
        # Check if the entered language is supported.
        try:
            assert self.language in self.json_files
        except AssertionError:
            raise NotImplementedError('Unsupported language!')
        
        self.json_path = os.path.join(self.this_dir, 'data', self.json_files[self.language])
        with open(self.json_path) as f:
            # Load the lexicon.
            self.lexicon = {kind: set(words) for kind, words in json.load(f).items()}
        self.tagger = TreeTagger(language=self.language)
        
        if language == 'english':
            # English is the standard in NLTK
            from nltk.tokenize import sent_tokenize
            self.sent_tokenize = sent_tokenize
        else:
            # Other languages have to be loaded using Pickle.
            pickle_path = self.tokenizers[language]
            self.sent_tokenize = nltk.data.load(pickle_path).tokenize
    
    def prefix_check(self, word_form, prefixes):
        "Check whether a word starts with one of several prefixes."
        for pref in prefixes:
            if word_form.startswith(pref):
                return True, pref
        return False, None
    
    def suffix_check(self, word_form, prefixes):
        "Check whether a word starts with one of several prefixes."
        for suff in suffixes:
            if word_form.endswith(suff):
                return True, suff
        return False, None
    
    def negation_status(word, pos, lemma, use_affixes=False):
        """
        Checks whether the word is a negation or not.
        Returns truth value and kind of negation.
        """
        word = word.lower()
        match = False
        kind = None
        if word in self.lexicon["WHOLEWORD"]:
            match = True
            kind = 'wholeword'
        elif lemma in self.lexicon["LEMMA"]:
            match = True
            kind = 'lemma'
        elif use_affixes:
            if pos.lower().startswith('v'):
                # Check verbs.
                # Check for negative prefix.
                prefixed, prefix = self.prefix_check(word, self.lexicon["VERB_STARTSWITH"])
                if prefixed:
                    match = True
                    kind = 'verb-prefix-' + prefix
            elif pos.lower.startswith('n'):
                # Check for negative prefix.
                prefixed, prefix = self.prefix_check(word, self.lexicon["NOUN_STARTSWITH"])
                if prefixed:
                    match = True
                    kind = 'noun-prefix-' + prefix
            elif pos.lower() in {'adj', 'jj'}:
                # Check adjectives.
                # Check for negative prefix.
                prefixed, prefix = self.prefix_check(word, self.lexicon["ADJ_STARTSWITH"])
                if prefixed:
                    match = True
                    kind = 'adj-prefix-' + prefix
                # Check for negative suffix.
                suffixed, suffix = self.suffix_check(word, self.lexicon["ADJ_ENDSWITH"])
                if suffixed:
                    match = True
                    kind = 'adj-suffix-' + suffix
        return match, kind
    
    def check_sentence(self, sentence, use_affixes=False):
        """
        Detect negations in a sentence. use_affixes yields many false positives,
        but might be useful to extend the negations file.
        """
        sentence_data = []
        tagged = self.tagger.tag(sentence)
        for idx, data in enumerate(tagged):
            word, pos, lemma = data
            match, kind = self.negation_status(word, pos, lemma, use_affixes)
            token = Token(idx, word, pos, lemma, match, kind)
            sentence_data.append(token)
        return sentence_data
    
    def check_text(self, text, use_affixes=False):
        """
        Detect negations in a text. use_affixes yields many false positives,
        but might be useful to extend the negations file.
        """
        return [check_sentence(sent, use_affixes) for sent in self.sent_tokenize(text)]
