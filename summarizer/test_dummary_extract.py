from .summary_extract import (split_sentences, split_words, 
                                keywords, title_score, length_score,
                                sentence_position, summarize)


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


final_title = "Fillon Scandal Indicts, Foremost, France’s Political Elite"

final_text = '''
PARIS — The president of the National Assembly does it. The president of the Senate defends it. Dozens of rank-and-file parliamentarians do it, too. Hiring your spouse, son or sister in France’s Parliament is perfectly legal.

So, with François Fillon, until recently France’s leading presidential candidate, in deep trouble for payments of nearly $1 million from the public payroll to his wife and children, many French politicians are asking: What’s the big deal?

The answer has, belatedly, come roaring back from much of the country’s press and public: They just don’t get it.

“Penelopegate,” a scandal named for Mr. Fillon’s wife, now threatens to sink the ambitions of a man who little more than a week ago seemed all but certain to become France’s next president.

Continue reading the main story
RELATED COVERAGE


François Fillon, French Presidential Hopeful, Faces Inquiry Over Payments to Wife JAN. 25, 2017

Graft Allegations Grow Against François Fillon, French Presidential Hopeful FEB. 1, 2017

A Candidate Rises on Vows to Control Islam and Immigration. This Time in France. NOV. 25, 2016

After Trump Win, Parallel Path Is Seen for Marine Le Pen of France’s Far Right NOV. 11, 2016
RECENT COMMENTS

CSD 1 hour ago
I hate to say this, but watch Marine LePen slip into the Presidency.
douzel 1 hour ago
Fillon used to asy : " I am Christian and gaulliste "
Susan 1 hour ago
I only wish that "Le Canard Enchaîné " which broke this story and so many others over the years had a real equivalent in the U.S., and more...
SEE ALL COMMENTS  WRITE A COMMENT
But the scandal has done more than add another volatile element to France’s presidential campaign. It has also tapped a wellspring of anger in the French electorate and called into question the standard operating procedures of the political class.

The outrage has buffeted the establishment, rendering it ever more vulnerable to the same angry populist forces that have already upset politics as usual from Washington to London to Rome.

France’s gilded political culture of immunity and privilege — free train and plane tickets, first-class travel, chauffeurs, all in a setting of marble and tapestries — can no longer be taken for granted, analysts warn.

The perception of a political structure run by and for elites who use it to enrich themselves — sometimes corruptly, but more often perfectly legally — is helping propel the far-right National Front candidate, Marine Le Pen.

“Nepotism is part of French institutional genetics,” said Matthieu Caron, an expert on government ethics at the University of Valenciennes. “It is unfortunately a ‘great’ French tradition.”

The scandal over Mr. Fillon, he added, is “making the National Front’s day,” even as Ms. Le Pen’s party, too, faces its own no-show employment scandal in the European Parliament.
'''


def test_summarize_final():
    assert len(summarize(final_title, final_text)) == 6