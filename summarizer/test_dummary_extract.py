from .summary_extract import split_sentences


test_sentence='''
Sentence 1. Sentence's 2 type.  I'm another sentence.
'''

def test_sentence_are_splitted():
    assert len(split_sentences(test_sentence) ) == 3

