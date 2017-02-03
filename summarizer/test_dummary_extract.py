from .summary_extract import (split_sentences, split_words, 
                                keywords, title_score, length_score,
                                sentence_position)


test_paragraph='''
Sentence 1. Sentence's 2 type.  I'm another sentence.
'''

def test_paragraph_is_splitted():
    assert len(split_sentences(test_paragraph) ) == 3


test_sentece = "This is a sentence."

def test_sentence_is_splitted():
    assert len(split_words(test_sentece)) == 4


test_sentence_for_keyword = "Man man dog goes to dog dog"

def test_keywords_extracted_from_sentence():
    keywords_ = keywords(test_sentence_for_keyword)
    assert round(keywords_["man"], 3) == round(2.0/7*1.5+1, 3)


title = ["this", "is", "title", "prime"]
sentence = ["new", "way", "to", "go"]
alt_sentence = ["new", "way", "to", "go", "title", "title", "prime", "prime"]

def test_title_score():
    assert title_score(title, sentence) == 0.0
    assert title_score(title, alt_sentence) == 2.0


def test_length_score():
    assert round(length_score(["javacript", "developer", "needed"]), 2) == 0.15



def test_sentence_position():
    assert round(sentence_position(2, 30), 2)== 0.17